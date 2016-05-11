# -*- coding: utf-8 -*-
"""
@author: Thomas Ost, Hanspeter Schmid 
"""

import numpy as np
import scipy as sp
import scipy.stats as spst
import matplotlib.pyplot as plt
import itertools
import csv
import xlrd
import os


#==============================================================================
# parameter
#==============================================================================
create_folder = False
directory     = 'bootstrapit_results'

#==============================================================================
# file handling
#==============================================================================

def set_folder_export_flag(export):
    global create_folder
    create_folder = export

def get_folder_export_flag():
    global create_folder
    return create_folder

def set_folder_name(name):
    global directory
    directory = name
    
def get_folder_name():
    global directory    
    return directory
    
def create_folder():
    #TODO: add gui prompt to choose directory    
    global directory
    if not os.path.exists(directory):
        os.makedirs(directory)    
    
    
    
def import_spreadsheet(filename):

       
    filetype_check = filename.split('.')
    filetype = filetype_check[-1]
        
    
    if filetype == 'csv':
        #call function parse csv
        row_list = parse_csv(filename)
    
    elif (filetype == 'xls') or (filetype == 'xlsx'):
        #call function pass xls
        row_list = parse_xls_xlsx(filename)
    
    else:
        print 'ERROR: wrong file type'
        return -1

    if column_or_row_ordered(row_list) == 'error':
        print 'ERROR: something is wrong with your spreadsheet layout'
        return -1
    
    elif column_or_row_ordered(row_list) == 'row':
        transposed_list = [list(x) for x in zip(*row_list)]        
        list_order  = transposed_list[0]
    
    elif column_or_row_ordered(row_list) == 'column':
        #transpose the lists
        list_order  = row_list[0]          
        row_list = [list(x) for x in zip(*row_list)]
        
    
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



def column_or_row_ordered(row_list):

    #if the first row consist of strings, these are probably the headers
    if all(isinstance(n, basestring) for n in row_list[0]):
        return 'column'
        
    elif all(isinstance(n, basestring) for n in (zip(*row_list)[0])):
        return 'row'    
    
    else:
        return 'error'


def parse_xls_xlsx(filename):

    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    
    row_list = []
    for row_ind in xrange(sheet.nrows):
        row_values = sheet.row_values(row_ind)
        row_list.append(row_values)
    
    return row_list

def parse_csv(filename):
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


def save_dictionary_to_csv(dict, filename):    
    if get_folder_export_flag():
        create_folder()
        filename = '/'.join((get_folder_name(), filename))

    
    with open(filename, 'wb') as f:
        w = csv.DictWriter(f, dict.keys())
        w.writeheader()
        w.writerow(dict)


def get_bootstrapped_average(bootstrapped_data, number_of_resamples, csv_export = False):
    #bootstrapped_data   = get_resampled_datasets(datasets, number_of_resamples)
    averaged_bootstrapped    = get_average_bootstrapped_data(bootstrapped_data)
    averaged_data            = {}
    
    for key, values in averaged_bootstrapped.iteritems():
        averaged_data[key]  =  np.mean(values, axis=0)
        
    if csv_export:
        save_dictionary_to_csv( averaged_data , 
                                'bootstrapped_average_results.csv')        

    return averaged_data  


def get_comparison_smaller_than(bootstrapped_data   , 
                                number_of_resamples , 
                                csv_export = False) :

    #get comparison smaller than all permutations
    #bootstrapped_data        = get_resampled_datasets(dataset, number_of_resamples)
    averaged_bootstrapped    = get_average_bootstrapped_data(bootstrapped_data)
    
    comparison_probabilities = {}
    
    #maybe use itertools-combinations here
    for p in itertools.permutations(averaged_bootstrapped.iteritems(),2):
        
        #compare each permutation of the averaged bootstraped value with eachother    
        average_comparison    = p[0][1] < p[1][1] 
        
        #compute the probabilities how often the first dataset value is smaller then the second    
        dataset_name_sequence = (p[0][0], p[1][0])    
        comparison_probabilities[' < '.join(dataset_name_sequence)] = np.float( np.sum( average_comparison ) ) / number_of_resamples

    if csv_export:
        save_dictionary_to_csv(comparison_probabilities, 'comparison_smaller_than_results.csv')            

    return comparison_probabilities



def get_significant_comparisons(  bootstrapped_data             , 
                                  number_of_resamples           , 
                                  significance_threshold = 0.05 , 
                                  csv_export = False)           : 


    #get comparison smaller than all permutations
    #bootstrapped_data        = get_resampled_datasets(dataset, number_of_resamples)
    averaged_bootstrapped    = get_average_bootstrapped_data(bootstrapped_data)
    
    comparison_probabilities = {}
    
    #maybe use itertools-combinations here
    for p in itertools.permutations(averaged_bootstrapped.iteritems(),2):
        
        #compare each permutation of the averaged bootstraped value with eachother    
        average_comparison    = p[0][1] < p[1][1] 
        
        #compute the probabilities how often the first dataset value is smaller then the second    
        dataset_name_sequence = (p[0][0], p[1][0])    
        comparison_probabilities[' < '.join(dataset_name_sequence)] = np.float( np.sum( average_comparison ) ) / number_of_resamples

    significant_comparison_probabilities = {}
    for  comparison, probability in comparison_probabilities.iteritems():
        if (probability <= significance_threshold):
            significant_comparison_probabilities[comparison] = probability
    
    if csv_export:
        save_dictionary_to_csv(significant_comparison_probabilities, 'signification_comparisons_results.csv')        
    
    return significant_comparison_probabilities


        
        


def get_ranking(bootstrapped_data, number_of_resamples, csv_export = False):

    #bootstrapped_data      = get_resampled_datasets(dataset, number_of_resamples)
    averaged_bootstrapped  = get_average_bootstrapped_data(bootstrapped_data)
    
    ranked_bootstrapped_dataset = get_ranking_by_size(averaged_bootstrapped, number_of_resamples)
    
    ranking_average =get_mean_after_ranking(ranked_bootstrapped_dataset)
    
    if csv_export:
        save_dictionary_to_csv(ranking_average, 'ranking_results.csv') 
    
    print ranking_average



def get_relative_average(bootstrapped_data            , 
                         number_of_resamples          , 
                         reference_name               , 
                         csv_export = False          ):
    
    #bootstrapped_data = get_resampled_datasets(dataset, number_of_resamples)    
     
    averaged_bootstrapped_datasets = {}
    reference                      = {}
    reference_avg                  = {}
    
    #normalise the reference dataset
    for key, bootstrapped_data_2D_Array in bootstrapped_data.iteritems():
        if key == reference_name:
            averaged_bootstrapped_datasets[key] = np.average(bootstrapped_data_2D_Array, axis = 0)
            reference[key] = bootstrapped_data_2D_Array / averaged_bootstrapped_datasets[key]
            reference_avg[key] = np.average(reference[key], axis = 0)
            
    #normalise every other dataset based on the average of the reference dset       
    for key, bootstrapped_data_2D_Array in bootstrapped_data.iteritems():
        if key != reference_name:
            reference[key] = bootstrapped_data_2D_Array / averaged_bootstrapped_datasets[reference_name]
            reference_avg[key] = np.average(reference[key], axis = 0)
    
    #average the normalised bootstrapped datasets
    total_average_dataset = {}
    for key, bootstrapped_data_1D_Array in reference_avg.iteritems():
        total_average_dataset[key] = np.average(bootstrapped_data_1D_Array)
    
    if csv_export:
        save_dictionary_to_csv(total_average_dataset, 'relative_average_results.csv') 
        
    return total_average_dataset
           


#==============================================================================
# helper functions
#==============================================================================


def get_ranking_by_size(bootstrapped_averaged_dataset, number_of_resamples):
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
     
def get_mean_after_ranking(ranked_dataset):
    
    #create dictionary with the mean value of all ranks for each dataset
    averaged_rank_bootstrapped_dataset = {}
    for key, ranked_array in ranked_dataset.iteritems():
        averaged_rank_bootstrapped_dataset[key]  =  np.mean(ranked_array, axis=0)
        
    return averaged_rank_bootstrapped_dataset

def get_resampled_datasets(dataset, resampling_numbers):
    bootstrapped_datasets = {}

    #loop efficiently through dictionary iterating one item at the time --> scalability for large datasets
    for key, data in dataset.iteritems():
        bootstrapped_datasets[key] = data[ np.int_( np.floor( sp.rand( len(data), resampling_numbers ) * len(data) ))]
    
    return bootstrapped_datasets



def get_average_bootstrapped_data(bootstrapped_dataset):
    
    #average all created bootstrap datasets for each dataset along FIXME: insert here axis!!!!! leaving you with a 1D-Array
    averaged_bootstrapped_datasets = {}

    for key, bootstrapped_data_2D_Array in bootstrapped_dataset.iteritems():
        averaged_bootstrapped_datasets[key] = np.average(bootstrapped_data_2D_Array, axis = 0)
        
    return averaged_bootstrapped_datasets


#==============================================================================
# plotting
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
















