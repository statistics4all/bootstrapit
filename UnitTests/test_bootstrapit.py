from unittest import TestCase

from bootstrapit import Bootstrapit


class TestBootstrapit(TestCase):
    def setUp(self):
        self.test_analysis = Bootstrapit('flicker.xlsx', number_of_resamples=10000)

    def test_mean(self):
        """
         Tests if the correct number of keys (experiment column names) is contained in the result dict and
         if the contained keys are identical to the column names.
        """
        mean_dict = self.test_analysis.mean()
        key_count = 0
        key_list = []
        for key in mean_dict:
            result_dict = mean_dict[key]
            for key, values in result_dict.items():
                print(key)
                key_list.append(key)
                key_count+= 1

        self.assertEqual(3, key_count)
        self.assertTrue(sorted(["Brown", "Green", "Blue"]) == sorted(key_list))

