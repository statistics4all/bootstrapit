from unittest import TestCase

from bootstrap_analysis import BootstrapAnalysis
from bootstrapper import Bootstrapper
from file_handling import FileHandling
import numpy as np


class TestBootstrapAnalysis(TestCase):

    def setUp(self):
        self.number_of_resamples = 10000

        # import dataset from file
        filename = 'flicker.xlsx'
        self.__fh = FileHandling()
        self.original_data_dict = self.__fh.import_spreadsheet(filename)

        # resample dataset
        self.__bootstrapper = Bootstrapper(self.original_data_dict, self.number_of_resamples)

        #init bootstrap analysis tools
        self.analysis = BootstrapAnalysis(self.__bootstrapper)


    def test_mean_dictionary_keys(self):
        """
        Tests if the correct number of keys (experiment column names) is contained in the result dict and
        if the contained keys are identical to the column names.
        """
        mean_dict = self.analysis.get_bootstrapped_mean()
        key_count = 0
        key_list = []
        for key in mean_dict:
            mean_data_dict = mean_dict[key]
            for key, values in mean_data_dict.items():
                print(key)
                key_list.append(key)
                key_count+= 1

        self.assertEqual(3, key_count)
        self.assertTrue(sorted(["Brown", "Green", "Blue"]) == sorted(key_list))


        def getshape(d):
            if isinstance(d, dict):
                return {k: getshape(d[k]) for k in d}
            else:
                # Replace all non-dict values with None.
                return None

        def shape_equal(d1, d2):
            return getshape(d1) == getshape(d2)



