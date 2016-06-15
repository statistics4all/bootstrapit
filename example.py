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
# Setting the number of resamplings of your data (number_of_resamples).
# 10000 is a good number to start and enough for a lot of cases, but you 
# can increase this number as you like. Increasing can lead to memory issues 
# when you have very very large datasets. You can play around and look at
# the results.
# if you wish to store your data in a folder you can set export to True. This
# will automatically store your analysis data in a subfolder where the 
# bootstrapît script is store. You can copy and paste it form there. 
# You also have to specify your export format. We support csv and xls at the
# moment.

#FIXME: add all arguments to the initialisation of the Bootstrapit class

analysis_1 = Bootstrapit('inputrow.xlsx'                    , 
                         number_of_resamples   = 10000      )


#Additional configurations

#file export and file type

# Here you can set your export data order. It is important that the names are
# exactly the same as in your data file, otherwise it will crash the program.
# If you want the same order as in the input file, simply delete these lines.

#TODO: add check export order functionality

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
                            
                            
analysis_1.file_export_config( store_data            = True                 ,
                               export_file_type      = 'xls'                ,
                               export_directory_name = 'bootstrap_results'  ,
                               export_order           = export_order_list   )


#add standard error of the mean to the results
analysis_1.use_sem = False




# Step 3: Run your analysis
"""
We configured our analysis in step 2 and are ready to compute. By initiialsing
the Bootstrapit analysis in step 2, the data has been automatically imported
and already been bootstrapped. This builds our base for getting some
information about the data.

Bootstrapit has a small featureset at the moment, but this already can be used
to compare the results with other statistical analysis methods.

Features:
- average
- relative average (normalised to a defined group of the dataset)
- ranking (ranking experiment, which ranks the data according to size)
- comparisons (gives us probabilities which can be used for significance tests)

These features have an individual description. So you can understand in detail
what is done in the background and how you can interpret your data. 
"""

# get average
analysis_1.get_bootstrapped_average()

# get relative average
analysis_1.get_relative_average( reference_name = 'WTY' )

# Compare the different mouse groups and compute the probabilites
analysis_1.get_comparison_smaller_than() 

# Print the probabilites if significant
analysis_1.get_significant_comparisons( significance_threshold = 0.08 )















