# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

import bootstrapit as bsi



#==============================================================================
# Enter your measured data
#==============================================================================
dataset, order_list = import_spreadsheet('inputrow.xlsx')

#bootstrapping configuration
N = 10000
bsi.set_number_of_resamples(N)
bsi.set_folder_export_flag(True)
bsi.set_file_export_flag(True)
bsi.set_file_type('xls')

#Hier den Ordnername eingeben anstatt Fibrosis
bsi.set_folder_name('Fibrosis') 


#set group name order for export --> Achtung muss mit den Importnamen im Excellsheet übereinstimmen!!!!
name_order_list = ['WTY', 'WTSO', 'WTTO', 'WTRO', 'MKOY', 'MKOSO', 'MKOTO', 'MCKY', 'MCKSO', 'MCKTO']
bsi.set_name_order(name_order_list)
#==============================================================================
#  get resample dataset (bootstrap)
#==============================================================================
bootstrapped_dataset = bsi.get_resampled_datasets(dataset)


#==============================================================================
# get average
#==============================================================================
bsi.get_bootstrapped_average( bootstrapped_dataset )

#==============================================================================
# get relative average
#==============================================================================
bsi.get_relative_average( bootstrapped_dataset , reference_name = 'WTY' )


#==============================================================================
# Compare the different mouse groups and compute the probabilites
#==============================================================================
bsi.get_comparison_smaller_than( bootstrapped_dataset ) 


#==============================================================================
# Print the probabilites if significant
#==============================================================================

bsi.get_significant_comparisons( bootstrapped_dataset          ,
                                 significance_threshold = 0.08 )















