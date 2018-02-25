# -*- coding: utf-8 -*-

"""
@author: Thomas Ost, Hanspeter Schmid 
"""

from bootstrapit import *
import matplotlib.pyplot as plt


from scipy import stats, integrate
import seaborn as sns
sns.set(color_codes=True)

"""
Example: The effect of iris colour in critical flicker frequency (CFF)
"""

analysis_1 = Bootstrapit('wafer.xlsx', number_of_resamples   = 10000 )

                            
# get mean and the standard error of the mean
original_mean = analysis_1.original_data_dict
mean         = analysis_1.mean()
sample_means = analysis_1.sample_means() #TODO: export sample means has to be implemented!#
SEM          = analysis_1.SEM()
analysis_1.export(mean, filename = "bootstrapit_results_mean.xlsx")


mean_dict = mean["mean"]

#plot distribution
alpha = 0.05
figure = plt.figure(99, facecolor='white')
#analysis_1.plot_distr(sample_means)
analysis_1.plot_two_sided_ci(sample_means, alpha)
plt.axvline(x=mean_dict["Wafer 1"], linestyle='-', color='r')
plt.axvline(x=mean_dict["Wafer 2"], linestyle='-', color='r')
plt.title("Distributions of the bootstrap sample means")
plt.xlabel("voltage (V)")
plt.ylabel("count")
plt.tight_layout()
sns.plt.show()



# #plot barchart
# figure = plt.figure(1, facecolor='white')
# plot = analysis_1.barchart(figure, mean)
#
# #add labels
# analysis_1.set_axis_label(plot, title = 'mean', xlabel = 'eye colour', ylabel = 'CFF (cycles/s)')
# plt.tight_layout()
# plt.show()
#
# #plot barchart with errorbar
# figure = plt.figure(2, facecolor='white')
# analysis_1.barchart(figure, mean, SEM)
# plt.tight_layout()
# plt.show()







