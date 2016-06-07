# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

# Step 1: import the bootstrapit module file
"""
This is the typical python import function. In order to use the functionality
of the bootstrapit module, we have to import it. This is because the module 
functions are written in the seperate file called "bootstrapit.py".
"""
from bootstrapit import *

# Step 2: Start a new analysis 
"""
A new analysis is started by calling Bootstrapit with the input data file. 
Bootstrapit can handle csv, xls, and xlsx file at the moment. Please organise
your data row, or column wise with the data title in the first entry.
See the example files: input_row_ordered.xls and input_column_ordered.xls for 
an example data organisation.

When your input file is in the same folder as the bootstrapit files then you
can just use the filename with the filetype extension --> filename.filetype 
(e.g. input.xls). If you store your data in a complete different folder then 
please enter the full file_path. This way bootstrapit can import your data 
correctly.
"""
# generating a new analysis workbench by defining your input file
analysis_1 = Bootstrapit('inputrow.xlsx')

# setting the number of random draws of your data (number of resampling)
# 10000 is a good number to start and enough for a lot of cases, but you 
# can increase this number as you like. This can lead to memory issues when 
# you have very very large datasets.
analysis_1.number_of_resamples = 10000

# if you wish to store your data in a folder you can set export to True. This
# will automatically store your analysis data in a subfolder where the 
# bootstrapît script is store. You can copy and paste it form there. 
# You also have to specify your export format. We support csv and xls at the
# moment.
analysis_1.use_directory  = True
analysis_1.use_file       = True
analysis_1.file_type      = 'xls'
analysis_1.directory_name = 'Fibrosis'
analysis_1.init_file_handling()#TODO: geht es auch ohne init???

# Here you can set your export data order. It is important that the names are
# exactly the same as in your data file, otherwise it will crash the program.
# If you want the same order as in the input file, simply delete these lines.
export_order_list        = ['WTY'   , #First
                            'WTSO'  , 
                            'WTTO'  , 
                            'WTRO'  , 
                            'MKOY'  , 
                            'MKOSO' , 
                            'MKOTO' , 
                            'MCKY'  , 
                            'MCKSO' , 
                            'MCKTO' ] #Last
                            
analysis_1.export_order  = export_order_list


#==============================================================================
# get average
#==============================================================================
analysis_1.get_bootstrapped_average()

#==============================================================================
# get relative average
#==============================================================================
analysis_1.get_relative_average( reference_name = 'WTY' )

#==============================================================================
# Compare the different mouse groups and compute the probabilites
#==============================================================================
analysis_1.get_comparison_smaller_than() 

#==============================================================================
# Print the probabilites if significant
#==============================================================================
analysis_1.get_significant_comparisons( significance_threshold = 0.08 )















