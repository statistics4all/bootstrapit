import itertools
import numpy as np
import scipy.stats as spst


class BootstrapAnalysis:
    def __init__(self, bootstrapper):
        self.__bootstrapper = bootstrapper
        self.__bootstrapped_data = self.__bootstrapper.bootstrapped_data

    def get_bootstrapped_mean(self):
        """
        The get_bootstrapped_mean method gets the mean of each dataset item averaged over each bootstrap sample.
        :return: returns a dictionary containing the results using the key "mean".
        """
        return_dict = {}
        averaged_data = {}
        averaged_bootstrapped = self.__get_average_bootstrapped_data(self.__bootstrapped_data)

        for key, values in averaged_bootstrapped.items():
            averaged_data[key] = np.mean(values, axis=0)

        return_dict['mean'] = averaged_data
        return return_dict

    def get_SEM(self):
        """
        Computes and returns the standard error of the mean
        :return: dictionary
        """
        return_dict = {}
        sem_results = {}

        #computes the sem of each resample (sem across rows)
        for key, bootstrapped_data_2D_Array in self.__bootstrapped_data.items():
            sem_results[key] = spst.stats.sem(bootstrapped_data_2D_Array)

        #computes the mean over all resampled sems
        for key, bootstrapped_data_2D_Array in sem_results.items():
            sem_results[key] = np.mean(bootstrapped_data_2D_Array)

        return_dict['SEM'] = sem_results
        return return_dict

    def get_bootstrapped_median(self):
        """
        The get_bootstrapped_median method gets the median of each dataset item of the median
        of each bootstrap sample.
        :return: returns a dictionary containing the results using the key "mean".
        """
        return_dict = {}
        resampling_medians = self.__get_median_bootstrapped_data(self.__bootstrapped_data)

        median_data = {}
        for key, values in resampling_medians.items():
            median_data[key] = np.median(values, axis=0)

        return_dict['median'] = median_data
        return return_dict

    def __get_value_comparison_by_size(self):

        spst.warnings.warn("Export of comparison by size does not work", RuntimeWarning)

        # get comparison smaller than all permutations
        averaged_bootstrapped \
            = self.__get_average_bootstrapped_data()

        comparison_probabilities = {}
        # maybe use itertools-combinations here
        for p in itertools.permutations(averaged_bootstrapped.items(), 2):
            # compare each permutation of averaged bootstraped value with eachother
            average_comparison = p[0][1] < p[1][1]

            # compute the probabilities how often the first dataset value is
            # smaller then the second
            dataset_name_sequence = (p[0][0], p[1][0])
            comparison_probabilities[' < '.join(dataset_name_sequence)] \
                = np.float(np.sum(average_comparison)) \
                  / self.number_of_resamples

        # TODO: ADD significant filtering to the export file.


        # filter out the signifiant comparisons
        if self.use_significance_sort:
            significant_comparison_probabilities = {}
            for comparison, probability in comparison_probabilities.items():
                if (probability <= self.significance_threshold):
                    significant_comparison_probabilities[comparison] = probability

            return comparison_probabilities, significant_comparison_probabilities

        return comparison_probabilities

    def get_ranking(self):

        averaged_bootstrapped \
            = self.__get_average_bootstrapped_data()

        ranked_bootstrapped_dataset \
            = self.__get_ranking_by_size(averaged_bootstrapped,
                                         self.number_of_resamples)

        ranking_average \
            = self.__get_mean_after_ranking(ranked_bootstrapped_dataset)

        return_dict = {}
        return_dict["ranking"] = ranking_average

        return return_dict

    def get_normalised_bootstrapped_mean(self, reference_name):

        # bootstrapped_data = get_resampled_datasets(dataset, number_of_resamples)

        averaged_bootstrapped_datasets = {}
        reference = {}
        reference_avg = {}

        # normalise the reference dataset
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            if key == reference_name:
                averaged_bootstrapped_datasets[key] \
                    = np.average(bootstrapped_data_2D_Array, axis=0)

                reference[key] = bootstrapped_data_2D_Array \
                                 / averaged_bootstrapped_datasets[key]

                reference_avg[key] = np.average(reference[key], axis=0)

        # normalise every other dataset based on the average of the reference dset
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            if key != reference_name:
                reference[key] = bootstrapped_data_2D_Array \
                                 / averaged_bootstrapped_datasets[reference_name]

                reference_avg[key] = np.average(reference[key], axis=0)

        # standard error of the mean of the rest of the dataset
        # FIXME: Implement correct SEM for referenced mean
        # standard_error_mean = self.get_standard_error_of_the_mean(reference)

        # average the normalised bootstrapped datasets
        total_average_dataset = {}
        for key, bootstrapped_data_1D_Array in reference_avg.items():
            total_average_dataset[key] = np.average(bootstrapped_data_1D_Array)

        return_dict = {}
        return_dict["normalised_mean"] = total_average_dataset
        # return_dict["SEM_NORM_MEAN"]   = standard_error_mean

        return return_dict

    def get_p_value(self):

        # dictionary of bootstrapped means
        true_mean_distr_dict = {}

        # compute mean of original dataset
        for key, values in self.original_data.items():
            true_mean_distr_dict[key] = np.mean(values, axis=0)

        # get bootstrapped means
        bs_mean_distr = self.__get_average_bootstrapped_data()

        # number of bootstrapped elements
        N = self.number_of_resamples

        # bootstrap p-value according to Davison and Hinkley (1997) Bootstrap Methods and their Application, p. 141
        # TODO: verify if this is a correct calculation of the p-value
        p_val_dict = {}
        for key, s_0 in true_mean_distr_dict.items():
            p_val_dict[key] = (1 + np.sum(bs_mean_distr[key] >= s_0)) / (N + 1)

        return p_val_dict

    def get_ranking_by_size(self, bootstrapped_averaged_dataset, number_of_resamples):
        # rank the averaged datasets accroding to their size compared to the other mouse datasets
        # smallest --> lowest rank
        # TODO: add option for biggest size lowest rank

        averaged_bootstrapped_2D_Array = np.zeros(shape=(number_of_resamples, len(bootstrapped_averaged_dataset)))
        key_order_list = []
        running_array_index = 0

        # this is by far not an efficiant or readable solution. But functional at the moment
        for key, average_bootstrapped_data in bootstrapped_averaged_dataset.items():
            averaged_bootstrapped_2D_Array[:, running_array_index] = average_bootstrapped_data
            key_order_list.append(key)
            running_array_index = running_array_index + 1

        # rank data across different datasets for comparison
        ranked_averaged_bootstrapped_dataset_2D_Array = np.apply_along_axis((lambda x: spst.rankdata(x)), 1,
                                                                            averaged_bootstrapped_2D_Array)

        # create new dictionary with ranked data
        ranked_averaged_bootstrapped_dataset = {}
        for column, key in zip(ranked_averaged_bootstrapped_dataset_2D_Array.T, key_order_list):
            ranked_averaged_bootstrapped_dataset[key] = column

        return ranked_averaged_bootstrapped_dataset

    def get_mean_after_ranking(self, ranked_dataset):

        # create dictionary with the mean value of all ranks for each dataset
        averaged_rank_bootstrapped_dataset = {}
        for key, ranked_array in ranked_dataset.items():
            averaged_rank_bootstrapped_dataset[key] = np.mean(ranked_array, axis=0)

        return averaged_rank_bootstrapped_dataset




    #private functions

    def __get_average_bootstrapped_data(self, bootstrapped_data):
        """
        Go through dictionary of categories and compute for each resample of each category the
        mean value across rows of the 2D-resampling-array (axis = 0).
        :param bootstrapped_data: resampling dictionary
        :return: dictionary containing the averaged resamplings of each category.
        """
        averaged_bootstrapped_datasets = {}

        for key, bootstrapped_data_2D_Array in bootstrapped_data.items():
            averaged_bootstrapped_datasets[key] = np.average(bootstrapped_data_2D_Array, axis=0)

        return averaged_bootstrapped_datasets

    def __get_median_bootstrapped_data(self, bootstrapped_data):
        """
        Go through dictionary of categories and compute for each resample of each category the
        median value across rows of the 2D-resampling-array (axis = 0).
        :param bootstrapped_data: resampling dictionary
        :return: dictionary containing the median resamplings of each category.
        """
        median_bootstrapped_datasets = {}

        for key, bootstrapped_data_2D_Array in bootstrapped_data.items():
            median_bootstrapped_datasets[key] = np.median(bootstrapped_data_2D_Array, axis=0)

        return median_bootstrapped_datasets