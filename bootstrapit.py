# -*- coding: utf-8 -*-
"""
@author: Thomas Ost, Hanspeter Schmid 
"""

import numpy as np
import scipy as sp
import scipy.stats as spst
from scipy import stats
import matplotlib.pyplot as plt
import itertools
import csv
import xlrd
import xlwt
from xlutils.copy import copy #replace with already installed package
import os
from file_handling import *
from plotting import *


#==============================================================================
# Bootstrapping
#==============================================================================

class Bootstrapit:
    def __init__(self, filename, number_of_resamples = 10000):

        self.number_of_resamples    = number_of_resamples
        self.bootstrapped_data      = {}
        self.use_sem                = False
        self.use_significance_sort  = False
        self.significance_threshold = 0.05
      
        self.fh  = FileHandling()
        self.original_data, self.export_order = self.fh.import_spreadsheet(filename)
        self.bootstrapped_data   = self.__get_resampled_datasets(self.original_data)
 
    def file_export_config(self                                         ,
                           store_data            = True                 ,
                           export_file_type      = 'xls'                ,
                           export_directory_name = 'bootstrap_results'  ,
                           export_order           = []                  ):
                               
        self.store_data     = store_data
        
        #Check if bootstrapit should export data
        if self.store_data:
            self.use_directory    = True
            self.use_file         = True
            self.fh.use_directory = self.use_directory
            self.fh.use_file      = self.use_file 
        else:
            self.use_directory    = False
            self.use_file         = False
            self.fh.use_directory = self.use_directory
            self.fh.use_file      = self.use_file 
            
        self.file_type            = export_file_type
        self.directory_name       = export_directory_name
        self.fh.file_type         = self.file_type
        self.fh.directory_name    = self.directory_name 
        
        if not export_order:        
            self.fh.export_order      = self.export_order
        else:
            self.fh.export_order      = export_order               
    
    
    def get_bootstrapped_mean( self ):
        
        averaged_bootstrapped \
            = self.__get_average_bootstrapped_data()
            
        averaged_data = {}        
        for key, values in averaged_bootstrapped.items():
            averaged_data[key]  =  np.mean(values, axis=0)
        
        
        
        standard_error_mean \
            = self.__get_standard_error_of_the_mean()
        
        
        #File export decisions
        if self.fh.use_file and self.use_sem:
            self.fh.save_dataset_and_sem_to_file( averaged_data          , 
                                                  standard_error_mean    , 
                                                  'bootstrapped_average' )
            return averaged_data, standard_error_mean
            
                                                  
        elif self.fh.use_file and not self.use_sem:
            self.fh.save_dataset_to_file( averaged_data          , 
                                          'bootstrapped_average' )
            return averaged_data

        else:
            
            if self.use_sem:
                return averaged_data, standard_error_mean
            else:
                return averaged_data                                 
        

    def get_bootstrapped_median( self ): 
        
        median_bootstrapped \
            = self.__get_median_bootstrapped_data()
            
        median_data = {}        
        for key, values in median_bootstrapped.items():
            median_data[key]  =  np.median(values, axis=0)
                   
        
         
        return median_data 


        
    def get_value_comparison_by_size( self ):
    
        #get comparison smaller than all permutations
        averaged_bootstrapped\
            = self.__get_average_bootstrapped_data()
        
        comparison_probabilities = {}
        #maybe use itertools-combinations here
        for p in itertools.permutations(averaged_bootstrapped.items() , 2):
            
        #compare each permutation of averaged bootstraped value with eachother    
            average_comparison    = p[0][1] < p[1][1] 
            
        #compute the probabilities how often the first dataset value is 
        #smaller then the second    
            dataset_name_sequence = (p[0][0], p[1][0])    
            comparison_probabilities[' < '.join(dataset_name_sequence)] \
                = np.float( np.sum( average_comparison ) )              \
                / self.number_of_resamples
                
                

    
        
        #TODO: ADD significant filtering to the export file.
    
        if self.fh.use_file:      
            self.fh.save_unordered_dictionary_to_xls(comparison_probabilities, 
                                            'comparison_by_size_results',
                                            column_offset = 0                )            
          
        #filter out the signifiant comparisons
        if self.use_significance_sort:
            significant_comparison_probabilities = {}
            for  comparison, probability in comparison_probabilities.items():
                if (probability <= self.significance_threshold):
                    significant_comparison_probabilities[comparison] = probability

                          
                        
            if self.fh.use_file:      
                self.fh.save_unordered_dictionary_to_xls(significant_comparison_probabilities, 
                                                'comparison_by_size_results',
                                                column_offset = 3           ,     
                                                mode = 'edit') 
            
            return comparison_probabilities, significant_comparison_probabilities
    
        return comparison_probabilities
    
        

    def get_ranking( self ):
    
        averaged_bootstrapped \
            = self.__get_average_bootstrapped_data()
        
        ranked_bootstrapped_dataset \
            = self.__get_ranking_by_size( averaged_bootstrapped          , 
                                        self.number_of_resamples )
        
        ranking_average \
            = self.__get_mean_after_ranking(ranked_bootstrapped_dataset)
        
        if self.fh.use_file:
              self.fh.save_dataset_to_file(ranking_average    ,  
                                            'ranking_results'  ) 
    
        return ranking_average



    def get_normalised_bootstrapped_mean( self , reference_name ):
        
        #bootstrapped_data = get_resampled_datasets(dataset, number_of_resamples)    
         
        averaged_bootstrapped_datasets = {}
        reference                      = {}
        reference_avg                  = {}
        
        #normalise the reference dataset
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            if key == reference_name:
                averaged_bootstrapped_datasets[key] \
                    = np.average(bootstrapped_data_2D_Array, axis = 0)
                    
                reference[key]     = bootstrapped_data_2D_Array        \
                                   / averaged_bootstrapped_datasets[key]
                               
                reference_avg[key] = np.average(reference[key], axis = 0)
                
                
        #normalise every other dataset based on the average of the reference dset       
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            if key != reference_name:
                reference[key] = bootstrapped_data_2D_Array                   \
                               / averaged_bootstrapped_datasets[reference_name]
                               

                reference_avg[key] = np.average(reference[key], axis = 0)
        
        
        #standard error of the mean of the rest of the dataset
        #FIXME: Implement correct SEM for referenced mean
        #standard_error_mean = self.get_standard_error_of_the_mean(reference)    
        
        #average the normalised bootstrapped datasets
        total_average_dataset = {}
        for key, bootstrapped_data_1D_Array in reference_avg.items():
            total_average_dataset[key] = np.average(bootstrapped_data_1D_Array)
        
        #File export decisions
        if self.fh.use_file and self.use_sem:
            self.fh.save_dataset_and_sem_to_file( total_average_dataset          , 
                                                  standard_error_mean    , 
                                                  'bootstrapped__relative_average' )
            return total_average_dataset, standard_error_mean
            
                                                  
        elif self.fh.use_file and not self.use_sem:
            self.fh.save_dataset_to_file( total_average_dataset          , 
                                          'bootstrapped__relative_average' )
            return total_average_dataset

        else:
            
            if self.use_sem:
                return total_average_dataset, standard_error_mean
            else:
                return total_average_dataset

        return total_average_dataset, standard_error_mean
           

#Private methods
#----------------------------------------------------------------------------------------------------------

    def __get_ranking_by_size(self, bootstrapped_averaged_dataset, number_of_resamples):
        #rank the averaged datasets accroding to their size compared to the other mouse datasets
        #smallest --> lowest rank
        #TODO: add option for biggest size lowest rank
    
        averaged_bootstrapped_2D_Array = np.zeros( shape=(number_of_resamples, len(bootstrapped_averaged_dataset)) )
        key_order_list = []
        running_array_index = 0
    
        #this is by far not an efficiant or readable solution. But functional at the moment
        for key, average_bootstrapped_data in bootstrapped_averaged_dataset.items():
            averaged_bootstrapped_2D_Array[:,running_array_index] = average_bootstrapped_data
            key_order_list.append(key)
            running_array_index = running_array_index + 1
    
        #rank data across different datasets for comparison
        ranked_averaged_bootstrapped_dataset_2D_Array = np.apply_along_axis(( lambda x: spst.rankdata(x) ), 1, averaged_bootstrapped_2D_Array)
    
        #create new dictionary with ranked data
        ranked_averaged_bootstrapped_dataset = {}
        for column, key in zip(ranked_averaged_bootstrapped_dataset_2D_Array.T, key_order_list):
            ranked_averaged_bootstrapped_dataset[key] = column
            
        return ranked_averaged_bootstrapped_dataset
         
    def __get_mean_after_ranking(self, ranked_dataset):
        
        #create dictionary with the mean value of all ranks for each dataset
        averaged_rank_bootstrapped_dataset = {}
        for key, ranked_array in ranked_dataset.items():
            averaged_rank_bootstrapped_dataset[key]  =  np.mean(ranked_array, axis=0)
            
        return averaged_rank_bootstrapped_dataset

    def __get_resampled_datasets(self, dataset):
        self.bootstrapped_datasets = {}
    
        #loop efficiently through dictionary iterating one item at the time --> scalability for large datasets
        for key, data in dataset.items():
            self.bootstrapped_datasets[key] = data[ np.int_( np.floor( sp.rand( len(data), self.number_of_resamples ) * len(data) ))]
        
        return self.bootstrapped_datasets



    def __get_average_bootstrapped_data(self):
        
        #average all created bootstrap datasets for each dataset along FIXME: insert here axis!!!!! leaving you with a 1D-Array
        averaged_bootstrapped_datasets = {}
    
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            averaged_bootstrapped_datasets[key] = np.average(bootstrapped_data_2D_Array, axis = 0)
            
        return averaged_bootstrapped_datasets
        
    def __get_median_bootstrapped_data(self):
        
        #average all created bootstrap datasets for each dataset along FIXME: insert here axis!!!!! leaving you with a 1D-Array
        median_bootstrapped_datasets = {}
    
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            median_bootstrapped_datasets[key] = np.median(bootstrapped_data_2D_Array, axis = 0)
            
        return median_bootstrapped_datasets

    def __get_standard_error_of_the_mean(self):
        
        sem_results = {}    
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.items():
            sem_results[key] = stats.sem(bootstrapped_data_2D_Array)
        
        for key, bootstrapped_data_2D_Array in sem_results.items():
            sem_results[key] = np.mean(bootstrapped_data_2D_Array)
            
        return sem_results





































