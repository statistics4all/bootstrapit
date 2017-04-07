# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx'                , 
                         number_of_resamples   = 10000 )

                            
# get mean --------------------------------------------------------------------
mean  = analysis_1.get_bootstrapped_mean()
SEM   = analysis_1.get_SEM()

#get median -------------------------------------------------------------------
median = analysis_1.get_bootstrapped_median() 

# get relative mean -----------------------------------------------------------
norm_mean = analysis_1.get_normalised_bootstrapped_mean( reference_name = 'Brown' )

#get ranking ------------------------------------------------------------------
ranking = analysis_1.get_ranking()
 
#File export 

export_order_list        = ['Brown' , #First
                            'Green' , 
                            'Blue'  ] #Last
                            
analysis_1.export(mean, median, norm_mean, ranking, filename = "bootstrapit_results.xls", order = export_order_list)


#simple barchart example ------------------------------------------------------

# set plot order the same as export order
plot_order = export_order_list

#plot barcharts
plot_barchart(mean  , plot_order, title = 'mean'  , xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )
plot_barchart(median, plot_order, title = 'median', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )
plot_barchart(ranking  , plot_order, title = 'rank'  , xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )



#==============================================================================
# Experimental Code
#==============================================================================

# Compare the different mouse groups and compute the probabilites

#significance level configuration gives you an additional exported row which
#shows you only the comparisons which are significant to your threshold
#NOTE: THIS FEATURE IS EXPERIMENTAL
# analysis_1.use_significance_sort  = True
# analysis_1.significance_threshold = 0.95
# analysis_1.get_value_comparison_by_size() 


