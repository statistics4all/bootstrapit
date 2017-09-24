from unittest import TestCase

from Bootstrapper import Bootstrapper
from file_handling import FileHandling


class TestBootstrapper(TestCase):

    self.data_dict = {} #FIXME: does not work this way check for correct class members in python
    self.bootstrapper = None

    def setUp(self):
        number_of_resamples = 10000
        filename = 'flicker.xlsx'


        fh = FileHandling()
        self.data_dict = self.fh.import_spreadsheet(filename)
        self.bootstrapper = Bootstrapper(self.data_dict, number_of_resamples)

    def test_matrix_dimensions(self):
        self.data_dict
