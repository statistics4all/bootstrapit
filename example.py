# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *
import matplotlib.pyplot as plt

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('flicker.xlsx', number_of_resamples   = 10000 )

                            
# get mean and the standard error of the mean
mean = analysis_1.mean()
SEM = analysis_1.SEM()
analysis_1.export(mean, filename = "bootstrapit_results_mean.xlsx")


#plot barchart
figure = plt.figure(1, facecolor='white')
plot = analysis_1.barchart(figure, mean)

#add labels
analysis_1.set_axis_label(plot, title = 'mean', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)')
plt.tight_layout()
plt.show()

#plot barchart with errorbar
figure = plt.figure(2, facecolor='white')
analysis_1.barchart(figure, mean, SEM)
plt.tight_layout()
plt.show()







