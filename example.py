# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

import bootstrapit as bsi


#==============================================================================
# Enter your measured data
#==============================================================================
dataset, order_list = import_spreadsheet('inputrow.xlsx')

#bootstrapping N times
N = 10000


#==============================================================================
#  get resample dataset (bootstrap)
#==============================================================================
bootstrapped_dataset = get_resampled_datasets(dataset, N)


#==============================================================================
# get average
#==============================================================================
bsi.get_bootstrapped_average( bootstrapped_dataset    , 
                              number_of_resamples = N , 
                              csv_export = True       )

#==============================================================================
# get relative average
#==============================================================================
bsi.get_relative_average( bootstrapped_dataset    , 
                          number_of_resamples = N , 
                          reference_name = 'WTY'  ,
                          csv_export = True       )

#==============================================================================
# ranking
#==============================================================================
bsi.get_ranking( bootstrapped_dataset    , 
                 number_of_resamples = N , 
                 csv_export = True       )

#==============================================================================
# Compare the different mouse groups and compute the probabilites
#==============================================================================
bsi.get_comparison_smaller_than( bootstrapped_dataset    , 
                                 number_of_resamples = N ,  
                                 csv_export = True       ) 


#==============================================================================
# Print the probabilites if significant
#==============================================================================

bsi.get_significant_comparisons( bootstrapped_dataset         , 
                                  number_of_resamples = N       , 
                                  significance_threshold = 0.08 ,
                                  csv_export = True             )



#==============================================================================
# Plot Data
#==============================================================================
#TODO: Plotting does not work at the moment
#plot_barchart( mean_ranked_averaged_bootstrapped_dataset , 
#               significant_comparison_probabilities      , 
#               plot_order                                )
















