#!/usr/bin/env python3
"""Compute review statistics from retained independent labels and adjudication."""
import argparse
import csv
import json
import math
from pathlib import Path

LABELS = {'SATD', 'non-SATD', 'uncertain', ''}


def read_sheet(path):
    with Path(path).open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    result = {}
    for row in rows:
        key = row['comment_id']
        if key in result or row['label'] not in LABELS:
            raise ValueError(f'Duplicate ID or invalid label in {path}')
        result[key] = row
    return result


def wilson(successes, n):
    if not n:
        return None
    z = 1.959963984540054
    proportion = successes / n
    denominator = 1 + z*z / n
    center = (proportion + z*z / (2*n)) / denominator
    half = z * math.sqrt(proportion*(1-proportion)/n + z*z/(4*n*n)) / denominator
    return [max(0, center-half), min(1, center+half)]


def agreement(first, second):
    common = set(first) & set(second)
    paired = [(first[k]['label'], second[k]['label']) for k in common
              if first[k]['label'] in {'SATD', 'non-SATD'}
              and second[k]['label'] in {'SATD', 'non-SATD'}]
    n = len(paired)
    result = dict(overlap_rows=len(common), paired_binary_n=n,
                  excluded_uncertain_or_blank=len(common)-n,
                  uncertain_handling='Exclude pairs with an uncertain or blank independent label.',
                  raw_agreement=None, expected_agreement=None, cohens_kappa=None)
    if n:
        observed = sum(a == b for a, b in paired) / n
        a_rate = sum(a == 'SATD' for a, b in paired) / n
        b_rate = sum(b == 'SATD' for a, b in paired) / n
        expected = a_rate*b_rate + (1-a_rate)*(1-b_rate)
        result.update(raw_agreement=observed, expected_agreement=expected,
                      cohens_kappa=(observed-expected)/(1-expected) if expected < 1 else None)
        if expected == 1:
            result['kappa_note'] = 'Undefined because expected agreement is 1.'
    return result


def calculate(admin, resolved, first, second):
    ids = {r['comment_id'] for r in admin}
    if len(ids) != len(admin) or set(resolved) != ids or set(first) != ids:
        raise ValueError('Primary and adjudication sheets must retain exactly the sampled IDs.')
    if not set(second) <= ids:
        raise ValueError('Second reviewer contains an unsampled comment.')
    groups = {}
    for name in ['strict', 'loose_only']:
        members = [r for r in admin if r['group'] == name]
        if not members:
            continue
        population = int(members[0]['population'])
        n = len(members)
        if any(int(r['population']) != population or int(r['sample_size']) != n for r in members):
            raise ValueError('Inconsistent sampling metadata.')
        labels = [resolved[r['comment_id']]['label'] for r in members]
        confirmed = labels.count('SATD')
        non = labels.count('non-SATD')
        uncertain = labels.count('uncertain')
        missing = labels.count('')
        reviewed = n - missing
        resolved_n = confirmed + non
        groups[name] = dict(population=population, sampled=n, reviewed=reviewed,
                            confirmed_satd=confirmed, non_satd=non,
                            unresolved_uncertain=uncertain, missing_labels=missing,
                            confirmed_fraction=confirmed/reviewed if reviewed else None,
                            precision=confirmed/n if not missing and not uncertain else None,
                            resolved_proportion=confirmed/resolved_n if resolved_n else None,
                            resolved_wilson_95=wilson(confirmed, resolved_n),
                            confirmed_fraction_bounds=[confirmed/n, (confirmed+uncertain)/n] if not missing else None,
                            note='Resolved-only proportions may be biased when uncertain cases remain.')
    total = sum(g['population'] for g in groups.values())
    weights = {name: g['population']/total for name, g in groups.items()} if total else {}
    all_complete = bool(groups) and all(g['missing_labels'] == 0 for g in groups.values())
    all_resolved = all_complete and all(g['unresolved_uncertain'] == 0 for g in groups.values())
    weighted = sum(weights[name]*g['precision'] for name, g in groups.items()) if all_resolved else None
    bounds = [sum(weights[name]*g['confirmed_fraction_bounds'][i] for name, g in groups.items())
              for i in range(2)] if all_complete else None
    independent_complete = bool(second) and all(r['label'] for r in first.values()) and all(r['label'] for r in second.values())
    return dict(status='labels_complete' if all_resolved and independent_complete else 'human_validation_pending',
                adjudication_status='resolved' if all_resolved else 'pending_or_uncertain',
                independent_labels_status='complete' if independent_complete else 'pending',
                group_statistics=groups, population_weights=weights,
                population_weighted_precision=weighted, population_weighted_confirmed_fraction_bounds=bounds,
                agreement=agreement(first, second), absolute_recall='not estimated',
                warning='Human identities and independence must be established outside this calculation. Do not substitute machine-generated labels.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, default=Path('results'))
    args = p.parse_args()
    root = args.directory
    with (root / 'sampling_admin.csv').open() as f:
        admin = list(csv.DictReader(f))
    first = read_sheet(root / 'reviewer_1.csv')
    second = read_sheet(root / 'reviewer_2_overlap.csv')
    manifest = json.loads((root / 'run_manifest.json').read_text())
    expected_overlap = manifest['overlap_size']
    if len(second) != expected_overlap:
        raise ValueError('Second-reviewer sheet must retain the full designated overlap.')
    if set(second) != set(manifest['overlap_comment_ids']):
        raise ValueError('Second-reviewer IDs differ from the designated independent overlap.')
    resolved = read_sheet(root / 'adjudication.csv')
    result = calculate(admin, resolved, first, second)
    (root / 'review_statistics.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])


if __name__ == '__main__':
    main()
