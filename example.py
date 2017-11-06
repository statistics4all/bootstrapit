# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx', number_of_resamples   = 10000 )

                            
# get mean --------------------------------------------------------------------
mean  = analysis_1.mean()
analysis_1.export(mean, filename = "bootstrapit_results_mean.xlsx")


#simple barchart example ------------------------------------------------------
#FIXME: plotting with order of import, plot_order should be optional
#plot barcharts
analysis_1.barchart(mean, title = 'mean', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)' )



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


