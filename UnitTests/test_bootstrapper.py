from unittest import TestCase

from Bootstrapper import Bootstrapper
from file_handling import FileHandling
import numpy as np


class TestBootstrapper(TestCase):

    def setUp(self):
        self.number_of_resamples = 10000
        filename = 'flicker.xlsx'

        self.bootstrapper = None
        fh = FileHandling()
        self.data_dict = fh.import_spreadsheet(filename)
        self.bootstrapper = Bootstrapper(self.data_dict, self.number_of_resamples)
        self.bootstrapped_dict = self.bootstrapper.bootstrapped_data


    def test_matrix_dimensions_are_correct(self):
        for key in self.data_dict:
            self.assertEqual(self.bootstrapped_dict[key].shape, (len(self.data_dict[key]),self.number_of_resamples))

    def test_values_are_part_of_original_sample(self):
        for key in self.data_dict:
            for value in np.nditer(self.bootstrapped_dict[key]):
                self.assertTrue(value in self.data_dict[key])
