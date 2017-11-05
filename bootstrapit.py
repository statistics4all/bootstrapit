# -*- coding: utf-8 -*-
"""
@author: Thomas Ost, Hanspeter Schmid 
"""

import numpy as np
from scipy import stats
import itertools
import warnings

from bootstrapper import Bootstrapper
from file_handling import FileHandling, FileType
from bootstrap_analysis import BootstrapAnalysis


class Bootstrapit:
    """
    The Bootstrapit class builds the API for the Bootstrapit application. The Methods inside this class can directly
    be used to interact with the application.
    """
    def __init__(self, filename, number_of_resamples=10000):

        """
        Initializing the Bootstrapit class executes the resampling of the imported dataset.
        :param filename: The filename including filepath to the import data file.
        :param number_of_resamples: The number of resamples to perform.
        """
        self.number_of_resamples = number_of_resamples


        # import dataset from file
        self.__fh = FileHandling()
        self.original_data_dict = self.__fh.import_spreadsheet(filename)

        # resample dataset
        self.__bootstrapper = Bootstrapper(self.original_data_dict, number_of_resamples)

        #init bootstrap analysis tools
        self.__analysis = BootstrapAnalysis(self.__bootstrapper)

    # TODO: Export bootstrapped data array
    def export(self, *export_datasets_dicts, filename="bootstrapit_results.xlsx"):

        """
        The export method does merge all data analysis result dictionaries and exports them using the FileHandler class.
        :param export_datasets_dicts: All result dictionaries from the bootstrapping analysis.
        :param filename: the export filename.
        """
        merged_dict = self.__merge_dicts(*export_datasets_dicts)

        filetype_check = filename.split('.')
        filetype = filetype_check[-1]
        filename = filetype_check[0]

        if filetype == "xlsx":
            self.__fh.file_type = FileType.XLSX
        elif filetype == "xls":
            self.__fh.file_type = FileType.XLS
        elif filetype == "csv":
            self.__fh.file_type = FileType.CSV
        else:
            print("Error: Unsupported file type.")

        self.__fh.file_name = filename
        self.__fh.export(merged_dict)

    def __merge_dicts(self, *dict_args):

        """
        Helper method to merge multiple result dictionaries.
        :param dict_args: List of dictionaries
        :return: The merged dictionary containing all results of the analysis.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def mean(self):
        return self.__analysis.get_bootstrapped_mean()