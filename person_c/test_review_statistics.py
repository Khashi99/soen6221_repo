"""Synthetic statistics tests; these labels are not human validation."""
import unittest
from review_statistics import agreement, calculate, wilson


def sheet(labels):
    return {str(i): {'label': label} for i, label in enumerate(labels)}


class Tests(unittest.TestCase):
    def test_wilson_known_extremes(self):
        self.assertIsNone(wilson(0, 0))
        self.assertAlmostEqual(wilson(0, 10)[1], .2775328, places=6)
        self.assertAlmostEqual(wilson(10, 10)[0], .7224672, places=6)

    def test_agreement_with_uncertainty(self):
        r = agreement(sheet(['SATD', 'SATD', 'non-SATD', 'non-SATD', 'uncertain']),
                      sheet(['SATD', 'non-SATD', 'SATD', 'non-SATD', 'SATD']))
        self.assertEqual(r['paired_binary_n'], 4)
        self.assertEqual(r['excluded_uncertain_or_blank'], 1)
        self.assertEqual(r['raw_agreement'], .5)
        self.assertEqual(r['cohens_kappa'], 0)

    def test_undefined_kappa(self):
        self.assertIsNone(agreement(sheet(['SATD']*3), sheet(['SATD']*3))['cohens_kappa'])
        self.assertIsNone(agreement(sheet(['']), sheet(['']))['cohens_kappa'])

    def test_weighted_precision_and_pending(self):
        admin = [dict(comment_id=str(i), group='strict' if i < 2 else 'loose_only',
                      population=90 if i < 2 else 10, sample_size=2) for i in range(4)]
        labelled = sheet(['SATD', 'SATD', 'non-SATD', 'non-SATD'])
        result = calculate(admin, labelled, labelled, {k: labelled[k] for k in ['0', '1']})
        self.assertAlmostEqual(result['population_weighted_precision'], .9)
        blank = sheet(['']*4)
        pending = calculate(admin, blank, blank, {k: blank[k] for k in ['0', '1']})
        self.assertIsNone(pending['population_weighted_precision'])
        self.assertEqual(pending['group_statistics']['strict']['missing_labels'], 2)

    def test_uncertainty_bounds(self):
        admin = [dict(comment_id=str(i), group='strict', population=100, sample_size=4) for i in range(4)]
        labels = sheet(['SATD', 'non-SATD', 'uncertain', 'uncertain'])
        r = calculate(admin, labels, labels, labels)
        self.assertIsNone(r['population_weighted_precision'])
        self.assertEqual(r['population_weighted_confirmed_fraction_bounds'], [.25, .75])
        self.assertEqual(r['group_statistics']['strict']['resolved_proportion'], .5)


if __name__ == '__main__':
    unittest.main()
