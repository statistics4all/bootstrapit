# -*- coding: utf-8 -*-

"""
Created on    Thu Nov 26 2015
Final version Thu Jan 14 2016

@author: Thomas Ost, Hanspeter Schmid 
"""

import bootstrapit as bsi

#TODOS
"""
- standard error of the mean für average, relative average und ranking

"""

#==============================================================================
# Enter your measured data
#==============================================================================

#dataset import --> has to be a csv file (save as csv in excel)
dataset, order_of_names = bsi.import_csv_data('input.csv')

#bootstrapping N times
N = 10000



#==============================================================================
#  get resample dataset (bootstrap)
#==============================================================================
bootstrapped_dataset = get_resampled_datasets(dataset, N)


#==============================================================================
# get average
#==============================================================================
bsi.get_bootstrapped_average( bootstrapped_dataset        , 
                              number_of_resamples = N     , 
                              csv_export = True           ,
                              name_order = order_of_names )

#==============================================================================
# get relative average
#==============================================================================
bsi.get_relative_average( bootstrapped_dataset        , 
                          number_of_resamples = N     , 
                          reference_name = 'WTY'      ,
                          csv_export = True           ,
                          name_order = order_of_names )

#==============================================================================
# ranking
#==============================================================================
bsi.get_ranking( bootstrapped_dataset        , 
                 number_of_resamples = N     , 
                 csv_export = True           ,
                 name_order = order_of_names )

#==============================================================================
# Compare the different mouse groups and compute the probabilites
#==============================================================================
bsi.get_comparison_smaller_than( bootstrapped_dataset    , 
                                 number_of_resamples = N ,  
                                 csv_export = True       ) 


#==============================================================================
# Print the probabilites if significant
#==============================================================================

bsi.get_signification_comparisons( bootstrapped_dataset         , 
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
















