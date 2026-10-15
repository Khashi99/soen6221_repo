"""All fixtures in this file are synthetic; none are pilot comments or patterns."""
import json
import tempfile
import unittest
from pathlib import Path
from satd_compare import (VARIANTS, compare, compile_config, extract_comments,
                          matches, sample_records)


def synthetic_config():
    patterns = [
        ('S', 'strict', 'marker', r'\bTODO\b'),
        ('L', 'loose_only', 'phrase', r'\bworkaround\b'),
        ('D', 'deprecated', 'marker', r'\bDEPRECATED\b'),
    ]
    return dict(status='ready', anchoring='every_line', frameworks=['SYNTHETIC'],
                scope='synthetic only', exclusions=[], patterns=[dict(
                    id=i, group=g, kind=k, regex=r, case_sensitive=False,
                    source='synthetic fixture; no paper or pilot attribution',
                    reason='test only') for i, g, k, r in patterns])


class Tests(unittest.TestCase):
    def test_independent_config(self):
        config = json.loads(Path(__file__).with_name('patterns.independent.json').read_text())
        compiled = compile_config(config)
        for phrase in ['TODO: fix', 'FIXME here', 'XXX investigate', 'HACK shortcut']:
            self.assertTrue(matches({'match_text': phrase}, VARIANTS[1], compiled, 'every_line'))
        for phrase in ['write_todos', 'todo_list', 'fixme_handler', 'deprecated_api', 'hardcoding_tool']:
            self.assertFalse(matches({'match_text': phrase}, VARIANTS[3], compiled, 'every_line'))
        for phrase in ['workaround', 'work around', 'work-around', 'hard-coded', 'hard coded',
                       'hardcoded', 'hardcoding', 'temporary solution', 'kludge', 'ugly']:
            self.assertTrue(matches({'match_text': phrase}, VARIANTS[3], compiled, 'every_line'))
            self.assertFalse(matches({'match_text': phrase}, VARIANTS[1], compiled, 'every_line'))

    def test_extraction(self):
        source = ('s = "# TODO string"\n'
                  '"""TODO docstring"""\n'
                  'x = 1  # TODO inline\n'
                  '# note\n# TODO adjacent\n\n# blank separated\n'
                  'if x:\n    # indented\n    pass\n# outer\n')
        blocks = extract_comments(source)
        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0]['start_line'], 3)
        self.assertEqual(blocks[0]['match_text'], 'TODO inline')
        self.assertEqual(blocks[1]['raw_text'], '# note\n# TODO adjacent')
        self.assertEqual(blocks[1]['end_line'], 5)
        self.assertFalse(any('docstring' in b['raw_text'] or 'string' in b['raw_text'] for b in blocks))

    def test_indent_and_code_break_groups(self):
        blocks = extract_comments('# one\n # different indent\nx=1\n # after code\n')
        self.assertEqual(len(blocks), 3)

    def test_tokenization_failure(self):
        with self.assertRaises(Exception):
            extract_comments('x = (\n# TODO broken\n')

    def test_variants_boundaries_and_anchoring(self):
        config = synthetic_config()
        patterns = compile_config(config)
        def hit(text, v, anchor='every_line'):
            return bool(matches({'match_text': text}, v, patterns, anchor))
        self.assertEqual([hit('DEPRECATED API', v) for v in VARIANTS], [True, False, False, False])
        self.assertEqual([hit('workaround here', v) for v in VARIANTS], [False, False, False, True])
        self.assertEqual([hit('note: TODO fix', v) for v in VARIANTS], [True, True, False, True])
        self.assertTrue(hit('note\nTODO fix', VARIANTS[2]))
        self.assertFalse(hit('note\nTODO fix', VARIANTS[2], 'first_line'))
        for text in ['write_todos', 'todo_list', 'TODO_tool', 'todometer']:
            self.assertFalse(hit(text, VARIANTS[1]))
        # Negations, quoted markers and optional enhancements remain candidates
        # under this synthetic baseline; human labels determine actual debt.
        for text in ['No TODO remains', 'the word "TODO"', 'TODO optional feature',
                     'TODO expected test failure', 'TODO fix debt in write_todos']:
            self.assertTrue(hit(text, VARIANTS[1]))
        self.assertEqual(len(matches({'match_text': 'TODO TODO'}, VARIANTS[1], patterns, 'every_line')), 2)

    def test_pending_config_rejected(self):
        with self.assertRaises(ValueError):
            compile_config({'status': 'pending_inputs'})

    def test_existing_human_labels_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            sheet = out / 'reviewer_1.csv'
            text = 'comment_id,label,reason\n1,SATD,existing human review\n'
            sheet.write_text(text)
            with self.assertRaisesRegex(ValueError, 'preserved'):
                compare(out / 'unused_corpus', out / 'unused_config', out)
            self.assertEqual(sheet.read_text(), text)

    def test_sampling_short_pool_and_repeatability(self):
        records = [{'comment_id': str(i), 'framework': 'SYNTHETIC'} for i in range(120)]
        full = {r['comment_id'] for r in records}
        strict = {str(i) for i in range(20)}
        a = sample_records(records, strict, full)
        self.assertEqual(a, sample_records(records[::-1], strict, full))
        selected, admin, overlap = a
        self.assertEqual(len(selected), 100)
        self.assertEqual(len({r['comment_id'] for r in selected}), 100)
        self.assertEqual(len(overlap), 30)
        self.assertEqual(sum(r['group'] == 'strict' for r in admin), 20)
        self.assertEqual(sum(r['group'] == 'loose_only' for r in admin), 80)
        self.assertEqual({r['probability'] for r in admin}, {1, .8})

    def test_population_smaller_than_100(self):
        records = [{'comment_id': str(i), 'framework': 'SYNTHETIC'} for i in range(7)]
        sample, admin, overlap = sample_records(records, {'0'}, {str(i) for i in range(7)})
        self.assertEqual(len(sample), 7)
        self.assertEqual(len(overlap), 7)
        self.assertTrue(all(r['probability'] == 1 for r in admin))

    def test_end_to_end_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            corpus, config = root / 'corpus.jsonl', root / 'config.json'
            rows = []
            for i in range(140):
                text = 'TODO fix' if i < 80 else ('workaround' if i < 120 else 'DEPRECATED routine documentation')
                rows.append(dict(comment_id=str(i), framework='SYNTHETIC',
                                 repository='synthetic/fixture', commit='a' * 40,
                                 path='fixture.py', start_line=i+1, end_line=i+1,
                                 raw_text='# ' + text, match_text=text, context=text,
                                 source_url='synthetic; no live source'))
            corpus.write_text(''.join(json.dumps(r) + '\n' for r in rows))
            config.write_text(json.dumps(synthetic_config()))
            compare(corpus, config, root / 'out')
            import csv
            with (root / 'out' / 'sensitivity.csv').open() as f:
                counts = list(csv.DictReader(f))
            self.assertEqual([int(r['candidates']) for r in counts[:4]], [100, 80, 80, 120])
            for name, n in [('reviewer_1.csv', 100), ('reviewer_2_overlap.csv', 30)]:
                with (root / 'out' / name).open() as f:
                    sheet = list(csv.DictReader(f))
                self.assertEqual(len(sheet), n)
                self.assertTrue(all(r['label'] == '' for r in sheet))
                self.assertNotIn('group', sheet[0])
            manifest = json.loads((root / 'out' / 'run_manifest.json').read_text())
            self.assertEqual(manifest['sample_size'], 100)
            self.assertEqual(manifest['coverage'], 80/120)
            self.assertEqual(manifest['precision'], 'pending human labels')


if __name__ == '__main__':
    unittest.main()
