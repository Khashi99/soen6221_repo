#!/usr/bin/env python3
"""Configurable SATD comparison; no built-in or reconstructed pilot dictionary."""
import argparse
import csv
import hashlib
import io
import json
import platform
import random
import re
import subprocess
import tokenize
from pathlib import Path

VERSION = '0.2.0'
SEED = 6221
VARIANTS = ('strict_plus_deprecated', 'strict_without_deprecated',
            'anchored_strict_without_deprecated', 'full_without_deprecated')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, rows, fields):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def extract_comments(source):
    """Actual # tokens; adjacent standalone lines merge only at equal indent."""
    lines = source.splitlines()
    blocks = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type != tokenize.COMMENT:
            continue
        line, col = tok.start
        prefix = lines[line - 1][:col]
        standalone = not prefix.strip()
        part = tok.string
        # Removing delimiters and leading whitespace affects the matching copy only.
        matching = part[1:].lstrip()
        if (blocks and standalone and blocks[-1]['standalone']
                and blocks[-1]['end_line'] == line - 1
                and blocks[-1]['indent'] == prefix):
            b = blocks[-1]
            b['end_line'] = line
            b['raw_text'] += '\n' + part
            b['match_text'] += '\n' + matching
        else:
            blocks.append(dict(start_line=line, end_line=line, raw_text=part,
                               match_text=matching, standalone=standalone,
                               indent=prefix))
    return [{k: v for k, v in b.items() if k not in ('indent', 'standalone')}
            for b in blocks]


def extract(manifest_path, out):
    manifest = json.loads(Path(manifest_path).read_text())
    if manifest.get('docstrings') != 'exclude':
        raise ValueError('This extractor excludes docstrings; use the pilot extractor if its scope differs.')
    exclusions = manifest['excluded_directory_names']
    if any(x in ('build', 'dist') for x in exclusions):
        raise ValueError('Do not blanket-exclude packages called build or dist.')
    records, errors = [], []
    for repo in manifest['repositories']:
        root = Path(repo['checkout']).resolve()
        sha = repo['commit']
        if not re.fullmatch(r'[0-9a-f]{40}', sha):
            raise ValueError('Every snapshot needs an exact 40-character commit SHA.')
        actual = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != sha:
            raise ValueError(f"Snapshot mismatch: {repo['framework']}")
        # Ensure tracked Python files match their pinned snapshot. Untracked files are excluded.
        changed = subprocess.check_output(['git', '-C', str(root), 'diff', 'HEAD', '--name-only'], text=True)
        if any(p.endswith('.py') for p in changed.splitlines()):
            raise ValueError(f"Modified Python sources: {repo['framework']}")
        paths = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z'], text=True).split('\0')
        for rel in sorted(p for p in paths if p.endswith('.py')):
            if any(part in exclusions for part in Path(rel).parts[:-1]):
                continue
            p = root / rel
            if not p.resolve().is_relative_to(root):
                raise ValueError(f'Source symlink escapes checkout: {rel}')
            try:
                with tokenize.open(p) as f:
                    source = f.read()
                blocks = extract_comments(source)
            except (tokenize.TokenError, SyntaxError, UnicodeError, OSError) as e:
                errors.append(dict(framework=repo['framework'], path=rel, error=str(e)))
                continue
            context_lines = source.splitlines()
            for b in blocks:
                identity = f"{repo['repository']}:{sha}:{rel}:{b['start_line']}:{b['end_line']}"
                lo, hi = b['start_line'], b['end_line']
                context = '\n'.join(context_lines[max(0, lo - 4):hi + 3])
                records.append(dict(b, comment_id=hashlib.sha256(identity.encode()).hexdigest(),
                                    framework=repo['framework'], repository=repo['repository'],
                                    commit=sha, path=rel, context=context,
                                    source_url=f"https://github.com/{repo['repository']}/blob/{sha}/{rel}#L{lo}-L{hi}"))
    out.mkdir(parents=True, exist_ok=True)
    (out / 'extraction_errors.json').write_text(json.dumps(errors, indent=2))
    if errors:
        raise ValueError(f'{len(errors)} extraction failures; see extraction_errors.json. Corpus not published.')
    (out / 'comments.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
    (out / 'extraction_manifest.json').write_text(json.dumps(dict(
        input=manifest, input_hash=digest(manifest_path), detector_version=VERSION,
        python_version=platform.python_version(), comment_blocks=len(records),
        corpus_hash=digest(out / 'comments.jsonl'), errors=0), indent=2))


def compile_config(config):
    if config.get('status') != 'ready':
        raise ValueError('Pattern configuration is pending; supply the exact pilot definitions.')
    if config.get('anchoring') not in ('first_line', 'every_line'):
        raise ValueError('Specify first_line or every_line anchoring for consecutive lines.')
    if not config.get('patterns'):
        raise ValueError('No patterns supplied.')
    compiled, ids = [], set()
    for p in config['patterns']:
        if p['id'] in ids:
            raise ValueError('Duplicate pattern ID.')
        ids.add(p['id'])
        if p['group'] not in ('strict', 'loose_only', 'deprecated'):
            raise ValueError('Invalid pattern group.')
        if p['kind'] not in ('marker', 'phrase'):
            raise ValueError('Invalid pattern kind.')
        if not p['regex'] or not p['source'] or not p['reason']:
            raise ValueError('Patterns require exact regex, source, and inclusion reason.')
        if not isinstance(p['case_sensitive'], bool):
            raise ValueError('Specify case sensitivity explicitly.')
        compiled.append((p, re.compile(p['regex'], 0 if p['case_sensitive'] else re.I)))
    if not any(p['group'] == 'deprecated' for p, _ in compiled):
        raise ValueError('Supply the exact DEPRECATED diagnostic definition.')
    return compiled


def matches(record, variant, compiled, anchoring):
    groups = {
        VARIANTS[0]: {'strict', 'deprecated'}, VARIANTS[1]: {'strict'},
        VARIANTS[2]: {'strict'}, VARIANTS[3]: {'strict', 'loose_only'},
    }[variant]
    text = record['match_text']
    hits = []
    for p, regex in compiled:
        if p['group'] not in groups:
            continue
        if variant == VARIANTS[2] and p['kind'] == 'marker':
            offset = 0
            segments = text.splitlines(keepends=True) if anchoring == 'every_line' else [text]
            for segment in segments:
                m = regex.match(segment)
                if m:
                    hits.append(dict(pattern_id=p['id'], span=[offset + m.start(), offset + m.end()]))
                offset += len(segment)
        else:
            hits.extend(dict(pattern_id=p['id'], span=list(m.span())) for m in regex.finditer(text))
    return hits


def sample_records(records, strict_ids, full_ids):
    rng = random.Random(SEED)
    pools = {
        'strict': sorted((r for r in records if r['comment_id'] in strict_ids), key=lambda r: r['comment_id']),
        'loose_only': sorted((r for r in records if r['comment_id'] in full_ids - strict_ids), key=lambda r: r['comment_id']),
    }
    n = {g: min(50, len(p)) for g, p in pools.items()}
    spare = min(100, len(full_ids)) - sum(n.values())
    for g in pools:
        take = min(spare, len(pools[g]) - n[g])
        n[g] += take
        spare -= take
    selected, admin = [], []
    for g, pool in pools.items():
        for r in rng.sample(pool, n[g]):
            selected.append(r)
            admin.append(dict(comment_id=r['comment_id'], group=g, framework=r['framework'],
                              population=len(pool), sample_size=n[g], probability=n[g] / len(pool)))
    rng.shuffle(selected)
    overlap = rng.sample(selected, min(30, len(selected)))
    return selected, admin, overlap


def compare(corpus_path, config_path, out):
    for filename in ['reviewer_1.csv', 'reviewer_2_overlap.csv', 'adjudication.csv']:
        sheet = out / filename
        if sheet.exists():
            with sheet.open(newline='', encoding='utf-8') as f:
                if any(row.get('label', '').strip() or row.get('reason', '').strip()
                       for row in csv.DictReader(f)):
                    raise ValueError('Existing review labels/reasons must be preserved. Use a new output directory.')
    config = json.loads(Path(config_path).read_text())
    compiled = compile_config(config)
    records = [json.loads(line) for line in Path(corpus_path).read_text().splitlines() if line.strip()]
    ids = set()
    required = ('comment_id', 'framework', 'repository', 'commit', 'path', 'start_line',
                'end_line', 'raw_text', 'match_text', 'context', 'source_url')
    for r in records:
        if any(k not in r for k in required):
            raise ValueError('Corpus is missing required metadata/context fields.')
        if r['comment_id'] in ids:
            raise ValueError('Duplicate comment ID; repeated text must retain distinct locations.')
        ids.add(r['comment_id'])
        if not re.fullmatch(r'[0-9a-f]{40}', r['commit']):
            raise ValueError('Corpus requires pinned commit SHAs.')
    frameworks = config['frameworks']
    if len(frameworks) != len(set(frameworks)) or any(r['framework'] not in frameworks for r in records):
        raise ValueError('Framework scope mismatch.')
    if not records:
        raise ValueError('Empty corpus.')
    populations, match_rows = {}, []
    for v in VARIANTS:
        populations[v] = set()
        for r in records:
            hits = matches(r, v, compiled, config['anchoring'])
            if hits:
                populations[v].add(r['comment_id'])
                match_rows.append(dict(r, variant=v, matches=hits))
    baseline = populations[VARIANTS[1]]
    rows = []
    for f in frameworks + ['TOTAL']:
        scope = {r['comment_id'] for r in records if f == 'TOTAL' or r['framework'] == f}
        for v in VARIANTS:
            candidates = populations[v] & scope
            rows.append(dict(framework=f, variant=v, comment_blocks=len(scope), candidates=len(candidates),
                             added_vs_strict=len((populations[v] - baseline) & scope),
                             removed_vs_strict=len((baseline - populations[v]) & scope),
                             candidates_per_1000_blocks=1000 * len(candidates) / len(scope) if scope else '',
                             status='measured'))
    selected, admin, overlap = sample_records(records, baseline, populations[VARIANTS[3]])
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / 'sensitivity.csv', rows, list(rows[0]))
    (out / 'matches.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in match_rows))
    fields = ['comment_id', 'framework', 'repository', 'commit', 'path', 'start_line', 'end_line',
              'raw_text', 'context', 'source_url', 'label', 'reason']
    def blinded(pool):
        return [{**{k: r[k] for k in fields if k in r}, 'label': '', 'reason': ''} for r in pool]
    write_csv(out / 'reviewer_1.csv', blinded(selected), fields)
    write_csv(out / 'reviewer_2_overlap.csv', blinded(overlap), fields)
    write_csv(out / 'sampling_admin.csv', admin, ['comment_id', 'group', 'framework', 'population', 'sample_size', 'probability'])
    total = len(populations[VARIANTS[3]])
    (out / 'run_manifest.json').write_text(json.dumps(dict(
        status='automated_complete_human_labels_pending', detector_version=VERSION,
        study=config.get('study', 'unspecified; consult input provenance'),
        detector_hash=digest(__file__), python_version=platform.python_version(), seed=SEED,
        configuration_hash=digest(config_path), corpus_hash=digest(corpus_path),
        scope=config['scope'], exclusions=config['exclusions'], anchoring=config['anchoring'],
        framework_commits=sorted({(r['framework'], r['commit']) for r in records}),
        denominator='all extracted comment blocks per framework; repeated text at different locations is retained',
        sample_population='strict_without_deprecated plus loose-only from full_without_deprecated',
        sample_size=len(selected), overlap_size=len(overlap),
        overlap_comment_ids=sorted(r['comment_id'] for r in overlap),
        coverage= len(baseline) / total if total else None,
        coverage_is_recall=False, absolute_recall='not estimated',
        precision='pending human labels', kappa='pending independent human labels'), indent=2))
    print(f'Compared {len(records)} blocks; exported {len(selected)} review rows and {len(overlap)} overlap rows.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    e = sub.add_parser('extract')
    e.add_argument('--manifest', required=True)
    e.add_argument('--out', required=True, type=Path)
    c = sub.add_parser('compare')
    c.add_argument('--corpus', required=True)
    c.add_argument('--config', required=True)
    c.add_argument('--out', required=True, type=Path)
    args = p.parse_args()
    if args.command == 'extract':
        extract(args.manifest, args.out)
    else:
        compare(args.corpus, args.config, args.out)


if __name__ == '__main__':
    main()
