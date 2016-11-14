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
Bootstrapit can handle csv, xls, and xlsx files at the moment. Please organise
your data row, or column wise with the data title in the first entry.
See the example files: inputrow.xls and inputcolumn.xls for 
an example data organisation.

When your input file is in the same folder as the bootstrapit files, you
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
# bootstrapît script is stored. You can copy and paste it form there. 
# You also have to specify your export format. We support csv and xls at the
# moment.



"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx'               , 
                         number_of_resamples   = 10000 )


#Additional configurations

#file export and file type

# You can set your export data order. It is important that the names are
# exactly the same as in your data file, otherwise it will crash the program.
# If you want the same order as in the input file, simply delete these lines
# and set export_order_list = []

export_order_list        = ['Brown' , #First
                            'Green' , 
                            'Blue'  ] #Last
                            
                            
analysis_1.file_export_config( store_data            = True                 ,
                               export_file_type      = 'xls'                ,
                               export_directory_name = 'bootstrap_results'  ,
                               export_order           = export_order_list   )


# Step 3: Run your analysis
"""
You configured our analysis in step 2 and you are now ready to compute. By 
initialsing the Bootstrapit analysis in step 2, the data has been automatically 
imported and has already been bootstrapped.

Bootstrapit has a small featureset at the moment, but this already can be used
to compare the results with other statistical analysis methods.

Features:
- mean
- median
- relative mean (normalised to a defined group of the dataset)
- ranking (ranking experiment, which ranks the data according to its values)
- comparisons (gives us probabilities which can be used for significance tests)

These features have an individual description. So you can understand in detail
what is done in the background and how you can interpret your data. 
"""



#add standard error of the mean to the results
#Works only for get mean at the moment value not for referenced/normalised mean.
analysis_1.use_sem = False

# get mean --------------------------------------------------------------------
analysis_1.get_bootstrapped_mean()

#get median -------------------------------------------------------------------
analysis_1.get_bootstrapped_median() 

# get relative mean -----------------------------------------------------------
analysis_1.get_normalised_bootstrapped_mean( reference_name = 'Brown' )

#get ranking ------------------------------------------------------------------
analysis_1.get_ranking()





#simple barchart example ------------------------------------------------------

mean   = analysis_1.get_bootstrapped_mean()
median = analysis_1.get_bootstrapped_median() 
rank   = analysis_1.get_ranking()

# set plot order the same as export order
plot_order = export_order_list

#plot barcharts
plot_barchart(mean  , plot_order, xlabel = 'eye colour', ylabel = 'mean'      )
plot_barchart(median, plot_order, xlabel = 'eye colour', ylabel = 'median'    )
plot_barchart(rank  , plot_order, xlabel = 'eye colour', ylabel = 'rank mean' )





#==============================================================================
# Experimental Code
#==============================================================================

# Compare the different mouse groups and compute the probabilites

#significance level configuration gives you an additional exported row which
#shows you only the comparisons which are significant to your threshold
#NOTE: THIS FEATURE IS EXPERIMENTAL
analysis_1.use_significance_sort  = True
analysis_1.significance_threshold = 0.95
analysis_1.get_value_comparison_by_size() 


