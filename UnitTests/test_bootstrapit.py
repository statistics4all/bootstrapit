from unittest import TestCase

from bootstrapit import Bootstrapit
import pandas as pd


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

    def test_export_single_result_dict(self):
        """
        Exports bootstrapping analysis results and imports the content of the created excel file.
        Checks if the values are equal (almost equal because of negligible floating point errors)
        """
        mean_dict = self.test_analysis.mean()
        export_filename = "UnitTestResults.xlsx"
        filepath = "bootstrapit_results/" + export_filename
        self.test_analysis.export(mean_dict, filename=export_filename)
        data_df = pd.read_excel(filepath)

        for key in mean_dict:
            result_dict = mean_dict[key]
            for category, values in result_dict.items():
                original_value = result_dict[category]
                exported_value = data_df.get_value(category, key)
                self.assertAlmostEqual(original_value, exported_value)







