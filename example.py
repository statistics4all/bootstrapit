# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx'               , 
                         number_of_resamples   = 10000 )


export_order_list        = ['Brown' , #First
                            'Green' , 
                            'Blue'  ] #Last
                            
                            
analysis_1.file_export_config( store_data            = True                 ,
                               export_file_type      = 'xls'                ,
                               export_directory_name = 'bootstrap_results'  ,
                               export_order           = export_order_list   )


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
plot_barchart(mean  , plot_order, title = 'mean'  , xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )
plot_barchart(median, plot_order, title = 'median', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )
plot_barchart(rank  , plot_order, title = 'rank'  , xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )





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


