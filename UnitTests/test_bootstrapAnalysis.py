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

    def check_keys_in_dict(self, dict):
        key_count = 0
        key_list = []
        for key in dict:
            result_dict = dict[key]
            for key, values in result_dict.items():
                print(key)
                key_list.append(key)
                key_count+= 1

        return key_list, key_count

    def test_mean_dictionary_keys(self):
        """
        Tests if the correct number of keys (experiment column names) is contained in the result dict and
        if the contained keys are identical to the column names.
        """
        mean_dict = self.analysis.get_bootstrapped_mean()
        key_list, key_count = self.check_keys_in_dict(mean_dict)

        self.assertEqual(3, key_count)
        self.assertTrue(sorted(["Brown", "Green", "Blue"]) == sorted(key_list))

    def test_median_dictionary_keys(self):
        """
        Tests if the correct number of keys (experiment column names) is contained in the result dict and
        if the contained keys are identical to the column names.
        """
        median_dict = self.analysis.get_bootstrapped_median()
        key_list, key_count = self.check_keys_in_dict(median_dict)

        self.assertEqual(3, key_count)
        self.assertTrue(sorted(["Brown", "Green", "Blue"]) == sorted(key_list))

    def test_SEM(self):
        """
        Tests if the correct number of keys (experiment column names) is contained in the result dict and
        if the contained keys are identical to the column names.
        """
        sem_dict = self.analysis.get_bootstrapped_median()
        key_list, key_count = self.check_keys_in_dict(sem_dict)

        self.assertEqual(3, key_count)
        self.assertTrue(sorted(["Brown", "Green", "Blue"]) == sorted(key_list))