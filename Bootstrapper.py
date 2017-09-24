import numpy as np
import scipy as sp


class Bootstrapper:
    """
    The Bootstrapper class is responsible for resampling imported datasets.
    """
    def __init__(self, data_dict, number_of_resamples):
        """
        Initializes the Boostrapper class by bootstrapping the input data dictionary n-times, based on the
        number_of_resamples.
        :param data_dict:
        :param number_of_resamples:
        """
        self.number_of_resamples = number_of_resamples
        self.data_dict = data_dict
        self.bootstrapped_data = self.__get_resampled_datasets(self.number_of_resamples)

    def __get_resampled_datasets(self, number_of_resamples):
        """
        Resamples datasets based on the number_of_resamples.
        :return: dictionary including a 2D Matrix with m = length of dataset; n = number_of_resamples for every input
        dataset.
        """
        bootstrapped_datasets = {}

        # loop efficiently through dictionary iterating one item at the time --> scalability for large datasets
        for key, data in self.data_dict.items():
            bootstrapped_datasets[key] = data[
                np.int_(np.floor(sp.rand(len(data), number_of_resamples) * len(data)))]

        return bootstrapped_datasets
