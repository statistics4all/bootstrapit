# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx', number_of_resamples   = 10000 )

                            
# get mean and the standard error of the mean
mean = analysis_1.mean()
SEM = analysis_1.SEM()
analysis_1.export(mean, filename = "bootstrapit_results_mean.xlsx")


#plot barchart
analysis_1.barchart(mean)

#plot barchart with errorbar
analysis_1.barchart(mean, SEM)

#add labels
#title = 'mean', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)'




