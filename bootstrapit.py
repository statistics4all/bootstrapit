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
import os



#TODO create a class called bootstrapit with parameters
#TODO create a class called file handling used for import and export of files
#TODO create a class called plotting for data visualisation

#==============================================================================
# bootstrapit class
#==============================================================================

class FileHandling:
    def __init__(self):
        
        self.use_directory       = False
        self.use_file            = False
        self. directory_name     = 'bootstrapit_results'
        self.file_type           = 'xlsx'
        self.file_name           = 'bootstrapit_results'      
        self.export_order        = []
        
            
    def create_folder(self):
        #TODO: add gui prompt to choose directory    
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)    
        
    def import_spreadsheet(self, filename):
               
        filetype_check = filename.split('.')
        filetype       = filetype_check[-1]
                   
        if filetype == 'csv':
            #call function parse csv
            row_list = self.parse_csv(filename)
        
        elif (filetype == 'xls') or (filetype == 'xlsx'):
            #call function pass xls
            row_list = self.parse_xls_xlsx(filename)
        
        else:
            print 'ERROR: wrong file type'
            return -1
    
        if self.column_or_row_ordered(row_list) == 'error':
            print 'ERROR: something is wrong with your spreadsheet layout'
            return -1
        
        elif self.column_or_row_ordered(row_list) == 'row':
            transposed_list = [list(x) for x in zip(*row_list)]        
            list_order      = transposed_list[0]
        
        elif self.column_or_row_ordered(row_list) == 'column':
            #transpose the lists
            list_order  = row_list[0]          
            row_list    = [list(x) for x in zip(*row_list)]
               
        else:
            print 'ERROR: something is wrong with your spreadsheet layout'
            return -1
            
        
        #change list to dictionary with first row as keys        
        datasets = {}
        for column in row_list:
            datasets[column[0]] = column[1:]
    
        new_dataset = {}
        for key, value in datasets.iteritems():
            
            #try to convert list to numpy float array        
            try:
                new_dataset[key] =  np.asarray(value, dtype=np.float)
            
            #when this fails there is possbily a empty cell
            except ValueError:
                data_array = np.array([], dtype = np.float)
                print 'Dataset contains empty cells, if this is ok than go on'
                for item in value:
                    #just add the elements which are not empty                
                    if item:                
                        data_array = np.append(data_array, item)
                        
                new_dataset[key] = data_array
        
        #return dataset as dictionary and list order as list
        return new_dataset, list_order  


    def column_or_row_ordered(self, row_list):
    
        #if the first row consist of strings, these are probably the headers
        if all(isinstance(n, basestring) for n in row_list[0]):
            return 'column'
            
        elif all(isinstance(n, basestring) for n in (zip(*row_list)[0])):
            return 'row'    
        
        else:
            return 'error'


    def parse_xls_xlsx(self, filename):
    
        book  = xlrd.open_workbook(filename)
        sheet = book.sheet_by_index(0)
        
        row_list = []
        for row_ind in xrange(sheet.nrows):
            row_values = sheet.row_values(row_ind)
            row_list.append(row_values)
        
        return row_list


    def parse_csv(self, filename):
        with open(filename) as csvfile:
                
                #check what delimiters the file uses
                dialect = csv.Sniffer().sniff( csvfile.read(1024) )
                
                #seek to the beginning of the file
                csvfile.seek(0)
                
                #read all rows and append them to a list  
                reader = csv.reader(csvfile,dialect)
                row_list = []
                for row in reader:
                    row_list.append(row)
                
        return row_list

    def save_dataset_to_file(self, data_dict, function_name):
            if self.file_type  == 'csv' :
                print 'csv file export'
                filename = '_'.join((self.directory_name,function_name))
                
                self.save_data_to_csv(data_dict    , 
                                          self.export_order , 
                                          filename          )           
                
            elif self.file_type == 'xls' :
                print 'xls file export'
                filename = '_'.join((self.directory_name,function_name))
                
                self.save_data_to_xls(data_dict    , 
                                          self.export_order , 
                                          filename          )
                
            elif self.file_type == 'xlsx':
                print 'xlsx file export'
                #TODO: implement xlsx export
            else:
                print 'ERROR: unknown export file type'
                return -1

    def save_dataset_and_sem_to_file(self, data_dict, sem_dict, function_name):
        if self.file_type  == 'csv' :
            print 'csv file export'
            filename = '_'.join((self.directory_name,function_name))
            
            self.save_data_with_sem_to_csv(data_dict    , 
                                           sem_dict          , 
                                           self.export_order , 
                                           filename          )           
            
        elif self.file_type == 'xls' :
            print 'xls file export'
        
            filename = '_'.join((self.directory_name,function_name))
                    
            self.save_data_with_sem_to_xls(data_dict         , 
                                           sem_dict          , 
                                           self.export_order , 
                                           filename          )
            
        elif self.file_type == 'xlsx':
            print 'xlsx file export'
            #TODO: implement xlsx export
        else:
            print 'ERROR: unknown export file type'
            return -1



    def save_dictionary_to_csv(self, dict, order_list, filename):
    
        csv_export_list = []
        
        for name in order_list:
            csv_export_list.append( dict[name] )
      
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
    
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow ( order_list       )
            
            if csv_export_list[0].size > 1:
                writer.writerows( csv_export_list )
            else:
                writer.writerow ( csv_export_list )
    
    def check_filename_for_slashes(self, filename):
        filename = filename.replace('/',' ')
        return filename

            
            
    def save_data_with_sem_to_csv(self       , 
                                  data_dict  , 
                                  sem_dict   , 
                                  order_list , 
                                  filename  ):
    
        csv_export_list     = []
        csv_sem_export_list = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'csv'))    
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            csv_sem_export_list.append( sem_dict[name]  )
            
    
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
    
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow ( order_list )
            
            if csv_export_list[0].size > 1:
                writer.writerows( csv_export_list )
            else:
                writer.writerow ( csv_export_list )
            
            writer.writerow(csv_sem_export_list)
        
        
    def save_data_with_sem_to_xls(self , 
                                  data_dict  , 
                                  sem_dict   , 
                                  order_list , 
                                  filename  ):
    
        csv_export_list     = []
        csv_sem_export_list = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls')) 
        
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            csv_sem_export_list.append( sem_dict[name]  )
        
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
        excell_list = []
        excell_list.append(order_list)
        excell_list.append(csv_export_list)
        excell_list.append(csv_sem_export_list)
        
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        for i, l in enumerate(excell_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filename)
    
    def save_data_to_csv(self       , 
                         data_dict  ,  
                         order_list , 
                         filename  ):
        
            csv_export_list     = []
            
            filename = self.check_filename_for_slashes(filename)
            filename = '.'.join((filename,'csv'))    
            
            if self.use_directory:
                self.create_folder()
                filename = '/'.join((self.directory_name, filename))    
            
            for name in order_list:
                csv_export_list.append    ( data_dict[name] )
            
            #check if there are more than one value in list to export
            if csv_export_list[0].size > 1:
                csv_export_list = [list(x) for x in zip(*csv_export_list)]  
        
        
            with open(filename, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow ( order_list )
                
                if csv_export_list[0].size > 1:
                    writer.writerows( csv_export_list )
                else:
                    writer.writerow ( csv_export_list )
                
                writer.writerow(csv_sem_export_list)
        
        
    def save_data_to_xls(self       , 
                         data_dict  , 
                         order_list , 
                         filename  ):
    
        csv_export_list     = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls'))    
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            
    
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
        excell_list = []
        excell_list.append(order_list)
        excell_list.append(csv_export_list)
 
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        for i, l in enumerate(excell_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filename)




    #TODO: integrate in general save storage function
    def save_unordered_dictionary_to_csv(self, dict, filename):
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'csv'))     
        filename = '_'.join((self.directory_name,filename)) 
        filename = self.check_filename_for_slashes(filename)
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))
    
        
        export_list = []
        for key, value in dict.iteritems():
            export_list.append([key,value])
        
        
        with open(filename, 'wb') as f:
            dw = csv.writer(f)
            dw.writerows(export_list)

    def save_unordered_dictionary_to_xls(self, dict, filename):
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls'))     
        filename = '_'.join((self.directory_name,filename)) 
        filename = self.check_filename_for_slashes(filename)
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))
    
        
        export_list = []
        for key, value in dict.iteritems():
            export_list.append([key,value])
        
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        for i, l in enumerate(export_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filename)




#==============================================================================
# Bootstrapping
#==============================================================================

class Bootstrapit:
    def __init__(self, filename, number_of_resamples = 10000):

        self.number_of_resamples = number_of_resamples
        self.bootstrapped_data   = {}
        self.use_sem             = False
      
        self.fh  = FileHandling()
        self.original_data, self.export_order = self.fh.import_spreadsheet(filename)
        self.bootstrapped_data   = self.get_resampled_datasets(self.original_data)
 
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
    
    
    def get_bootstrapped_average( self ):
        
        averaged_bootstrapped \
            = self.get_average_bootstrapped_data()
            
        averaged_data = {}        
        for key, values in averaged_bootstrapped.iteritems():
            averaged_data[key]  =  np.mean(values, axis=0)
        
        
        
        standard_error_mean \
            = self.get_standard_error_of_the_mean()
        
        
        #File export decisions
        if self.fh.use_file and self.use_sem:
            self.fh.save_dataset_and_sem_to_file( averaged_data          , 
                                                  standard_error_mean    , 
                                                  'bootstrapped_average' )
            return averaged_data, standard_error_mean
            
                                                  
        elif self.fh.use_file and not self.use_sem:
            self.fh.save_daset_to_file( averaged_data          , 
                                          'bootstrapped_average' )
            return averaged_data

        else:
            
            if self.use_sem:
                return averaged_data, standard_error_mean
            else:
                return averaged_data                                 
        




    def get_comparison_smaller_than( self ):
    
        #get comparison smaller than all permutations
        averaged_bootstrapped\
            = self.get_average_bootstrapped_data()
        
        comparison_probabilities = {}
        #maybe use itertools-combinations here
        for p in itertools.permutations(averaged_bootstrapped.iteritems() , 2):
            
        #compare each permutation of averaged bootstraped value with eachother    
            average_comparison    = p[0][1] < p[1][1] 
            
        #compute the probabilities how often the first dataset value is 
        #smaller then the second    
            dataset_name_sequence = (p[0][0], p[1][0])    
            comparison_probabilities[' < '.join(dataset_name_sequence)] \
                = np.float( np.sum( average_comparison ) )              \
                / self.number_of_resamples
    
        if self.fh.use_file:      
            self.fh.save_unordered_dictionary_to_xls(comparison_probabilities, 
                                            'comparison_smaller_than_results')            
    
        return comparison_probabilities



    def get_significant_comparisons( self , significance_threshold = 0.05 ): 
    
        #get comparison smaller than all permutations
        averaged_bootstrapped \
            = self.get_average_bootstrapped_data()
        
        comparison_probabilities = {}
        #maybe use itertools-combinations here
        for p in itertools.permutations(averaged_bootstrapped.iteritems(),2):
            
            #compare each permutation of the averaged bootstraped value 
            #with eachother    
            average_comparison    = p[0][1] < p[1][1] 
            
            #compute the probabilities how often the first dataset value is 
            #smaller then the second    
            dataset_name_sequence = (p[0][0], p[1][0])    
            comparison_probabilities[' < '.join(dataset_name_sequence)] \
                = np.float( np.sum( average_comparison ) )              \
                / self.number_of_resamples
    
        significant_comparison_probabilities = {}
        for  comparison, probability in comparison_probabilities.iteritems():
            if (probability <= significance_threshold):
                significant_comparison_probabilities[comparison] = probability
        
        if self.fh.use_file:
             self.fh.save_unordered_dictionary_to_xls(                        \
                                         significant_comparison_probabilities , 
                                             'significant_comparisons_results')        
        
        return significant_comparison_probabilities


        

    def get_ranking( self ):
    
        averaged_bootstrapped \
            = self.get_average_bootstrapped_data()
        
        ranked_bootstrapped_dataset \
            = self.get_ranking_by_size( averaged_bootstrapped          , 
                                        self.number_of_resamples )
        
        ranking_average \
            = self.get_mean_after_ranking(ranked_bootstrapped_dataset)
        
        if self.fh.use_file:
              self.fh.save_dataset_to_file(ranking_average    ,  
                                            'ranking_results'  ) 
    
        print ranking_average



    def get_relative_average( self , reference_name ):
        
        #bootstrapped_data = get_resampled_datasets(dataset, number_of_resamples)    
         
        averaged_bootstrapped_datasets = {}
        reference                      = {}
        reference_avg                  = {}
        
        #normalise the reference dataset
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.iteritems():
            if key == reference_name:
                averaged_bootstrapped_datasets[key] \
                    = np.average(bootstrapped_data_2D_Array, axis = 0)
                    
                reference[key]     = bootstrapped_data_2D_Array        \
                                   / averaged_bootstrapped_datasets[key]
                               
                reference_avg[key] = np.average(reference[key], axis = 0)
                
                
        #normalise every other dataset based on the average of the reference dset       
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.iteritems():
            if key != reference_name:
                reference[key] = bootstrapped_data_2D_Array                   \
                               / averaged_bootstrapped_datasets[reference_name]
                               

                reference_avg[key] = np.average(reference[key], axis = 0)
        
        
        #standard error of the mean of the rest of the dataset
        #FIXME: Implement correct SEM for referenced mean
        #standard_error_mean = self.get_standard_error_of_the_mean(reference)    
        
        #average the normalised bootstrapped datasets
        total_average_dataset = {}
        for key, bootstrapped_data_1D_Array in reference_avg.iteritems():
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
           


#==============================================================================
# helper functions Bootstrapit
#==============================================================================


    def get_ranking_by_size(self, bootstrapped_averaged_dataset, number_of_resamples):
        #rank the averaged datasets accroding to their size compared to the other mouse datasets
        #smallest --> lowest rank
        #TODO: add option for biggest size lowest rank
    
        averaged_bootstrapped_2D_Array = np.zeros( shape=(number_of_resamples, len(bootstrapped_averaged_dataset)) )
        key_order_list = []
        running_array_index = 0
    
        #this is by far not an efficiant or readable solution. But functional at the moment
        for key, average_bootstrapped_data in bootstrapped_averaged_dataset.iteritems():
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
         
    def get_mean_after_ranking(self, ranked_dataset):
        
        #create dictionary with the mean value of all ranks for each dataset
        averaged_rank_bootstrapped_dataset = {}
        for key, ranked_array in ranked_dataset.iteritems():
            averaged_rank_bootstrapped_dataset[key]  =  np.mean(ranked_array, axis=0)
            
        return averaged_rank_bootstrapped_dataset

    def get_resampled_datasets(self, dataset):
        self.bootstrapped_datasets = {}
    
        #loop efficiently through dictionary iterating one item at the time --> scalability for large datasets
        for key, data in dataset.iteritems():
            self.bootstrapped_datasets[key] = data[ np.int_( np.floor( sp.rand( len(data), self.number_of_resamples ) * len(data) ))]
        
        return self.bootstrapped_datasets



    def get_average_bootstrapped_data(self):
        
        #average all created bootstrap datasets for each dataset along FIXME: insert here axis!!!!! leaving you with a 1D-Array
        averaged_bootstrapped_datasets = {}
    
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.iteritems():
            averaged_bootstrapped_datasets[key] = np.average(bootstrapped_data_2D_Array, axis = 0)
            
        return averaged_bootstrapped_datasets

    def get_standard_error_of_the_mean(self):
        
        sem_results = {}    
        for key, bootstrapped_data_2D_Array in self.bootstrapped_data.iteritems():
            sem_results[key] = stats.sem(bootstrapped_data_2D_Array)
        
        for key, bootstrapped_data_2D_Array in sem_results.iteritems():
            sem_results[key] = np.mean(bootstrapped_data_2D_Array)
            
        return sem_results






















#==============================================================================
# plotting FIXME: Just sketching the functionality has to be changed for
#                 a nicer API
#==============================================================================



SPACE = ' '

def stars(p):
    """
    this is a so called function which can be used in your normal code by 
    writing start(data) and as an argument you insert your probabilities.
    it will return a string (a string is a set of characters) which
    contains the stars
    """
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "-"

def hashtags(p):
    """
    this is a so called function which can be used in your normal code by 
    writing start(data) and as an argument you insert your probabilities.
    it will return a string (a string is a set of characters) which
    contains the stars
    """
    if p < 0.0001:
        return "####"
    elif (p < 0.001):
        return "###"
    elif (p < 0.01):
        return "##"
    elif (p < 0.05):
        return "#"
    else:
        return "-"

#bootstrapping




#plotting
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
             
# Tableau Color Blind 10
tableau20blind = [(0, 107, 164), (255, 128, 14), (171, 171, 171), (89, 89, 89),
             (95, 158, 209), (200, 82, 0), (137, 137, 137), (163, 200, 236),
             (255, 188, 121), (207, 207, 207)]
  
# Rescale to values between 0 and 1 
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)
for i in range(len(tableau20blind)):  
    r, g, b = tableau20blind[i]  
    tableau20blind[i] = (r / 255., g / 255., b / 255.)


def plot_barchart(dataset, significance_dataset, plot_order):
    
    #sort according to plot_order
    data = []
    for name in plot_order:
        data.append(dataset.get(name))
           
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    
    my_colors = []
    
    for index in range(len(group_list[0])):
        my_colors.append(tableau20[index])
    
    barchart = ax.bar( range( len(dataset) ), data, align = 'center', color=my_colors)    
    plt.xticks( range( len(dataset) ) , plot_order, rotation = 45)
    ax.set_ylabel('Rank')
    ax.set_title('Bootstrapping Results Fibrosis')

        #inter group signifikance and in group significance  
    for key, probability in significance_dataset.iteritems():
        compared_dataset_names = key.split(' < ')
        
        #serch key pair in group        
        position_key1 = find_name_position(compared_dataset_names[0])
        position_key2 = find_name_position(compared_dataset_names[1])
        
        #if in group do stars
        if position_key1[0] == position_key2[0]:
            bar_select_counter= 0
            for rect in barchart:
                if (plot_order[bar_select_counter] == compared_dataset_names[0]) or (plot_order[bar_select_counter] == compared_dataset_names[1]):
                    #maximum and minim height of rectancles
                    y_max = max( dataset[compared_dataset_names[0]], dataset[compared_dataset_names[1]] ) + 0.35 # TODO: create constant for 0.35 offset
                    y_min = min( dataset[compared_dataset_names[0]], dataset[compared_dataset_names[1]] ) + 0.35
                    distance = abs( plot_order.index(compared_dataset_names[0]) -  plot_order.index(compared_dataset_names[1]) )
                    print bar_select_counter
                    print compared_dataset_names[0]
                    ax.annotate("", 
                                xy=(bar_select_counter+0.0, y_max)                                                , #first point
                                xycoords='data'                                                                    ,
                                xytext=(bar_select_counter+1.00, y_max)                                            , #second point offset by 1
                                textcoords='data'                                                                  ,
                                arrowprops=dict(arrowstyle="-", ec='#000000', connectionstyle="bar,fraction=0.2"))
                           
                           
                    ax.text(bar_select_counter+0.5, y_max + 0.4, stars(probability),
                            horizontalalignment='center',
                            verticalalignment='center')
                    
                    #break out of loop
                    break
                        
                bar_select_counter = bar_select_counter + 1
        
        #else do hashtag
        else:
            label_select_counter= 0
            for rect in barchart:               
                if label_select_counter == ( ( (position_key2[0] + 1)  *  (position_key2[1] + 1) ) - 1 ):
                    #FIXME hashtags should just be printed once
                    print label_select_counter
                    height = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                    hashtags(probability),
                    ha='center', va='bottom')
                
                label_select_counter = label_select_counter + 1
    
  




def find_name_position(name):
    for group_index, item in enumerate(group_list):
        for index, element in enumerate(item):
            if element == name:
                first_key_index = (group_index,index)
                return first_key_index
    else:
        return(None)
        



def value_label(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%0.1f' % height,
                ha='center', va='bottom')

def significance_labeling_inter_group(rects, p_value):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                hashtags(p_value),
                ha='center', va='bottom')


#value_label(bar)
















