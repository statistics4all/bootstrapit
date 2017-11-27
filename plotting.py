import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# FIXME: Just sketching the functionality has to be changed for a nicer API
class Plotting():
    def __init__(self, plot_order):
        self.SPACE = ' '
        self.plot_order = plot_order


    def plot_barchart(self, dataset_dict, errorbar = {}):
        """
        Barchart plots the input dataset dictionary according to the key order in
        the input plot_order variable. It also plots the value of the specific key
        above the center of the corresponding bar.
        :param dataset_dict: The dictionary of your dataset (e.g. mean)
        :param errorbar: A dictionary containing errors (e.g. SEM) corresponding to the dataset.
        """

        data = self.__set_plot_order(dataset_dict)

        #set-up figure
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)

        #get barchart
        if errorbar:
            errobar_list = self.__set_plot_order(errorbar)
            barchart = ax.bar(range(len(self.plot_order)), data, align='center', yerr = errobar_list)
        else:
            barchart = ax.bar( range( len(self.plot_order) ), data, align = 'center')

        #set labels
        plt.xticks(range(len(self.plot_order)), self.plot_order, rotation = 45)
        self.__set_barchart_value_labels(ax, barchart)

        plt.show()
        return plt

    #this is only for experimental trials and not functional
    def plot_barchart_sign(self, dataset, significance_dataset, plot_order):

            #inter group signifikance and in group significance
        for key, probability in significance_dataset.items():
            compared_dataset_names = key.split(' < ')

            #serch key pair in group
            position_key1 = find_name_position(compared_dataset_names[0])
            position_key2 = find_name_position(compared_dataset_names[1])

            #if in group do stars
            if position_key1[0] == position_key2[0]:
                bar_select_counter= 0
                for rect in barchart:
                    if (plot_order[bar_select_counter] == compared_dataset_names[0]) or (plot_order[bar_select_counter] == compared_dataset_names[1]):
                        #maximum and minim height of rectancles
                        y_max = max( dataset[compared_dataset_names[0]], dataset[compared_dataset_names[1]] ) + 0.35 # TODO: create constant for 0.35 offset
                        y_min = min( dataset[compared_dataset_names[0]], dataset[compared_dataset_names[1]] ) + 0.35
                        distance = abs( plot_order.index(compared_dataset_names[0]) -  plot_order.index(compared_dataset_names[1]) )
                        print (bar_select_counter)
                        print (compared_dataset_names[0])
                        ax.annotate("",
                                    xy=(bar_select_counter+0.0, y_max)                                                , #first point
                                    xycoords='data'                                                                    ,
                                    xytext=(bar_select_counter+1.00, y_max)                                            , #second point offset by 1
                                    textcoords='data'                                                                  ,
                                    arrowprops=dict(arrowstyle="-", ec='#000000', connectionstyle="bar,fraction=0.2"))


                        ax.text(bar_select_counter+0.5, y_max + 0.4, stars(probability),
                                horizontalalignment='center',
                                verticalalignment='center')

                        #break out of loop
                        break

                    bar_select_counter = bar_select_counter + 1

            #else do hashtag
            else:
                label_select_counter= 0
                for rect in barchart:
                    if label_select_counter == ( ( (position_key2[0] + 1)  *  (position_key2[1] + 1) ) - 1 ):
                        #FIXME hashtags should just be printed once
                        print (label_select_counter)
                        height = rect.get_height()
                        ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                        hashtags(probability),
                        ha='center', va='bottom')

                    label_select_counter = label_select_counter + 1

    def set_axis_labels(self, ax, title, xlabel, ylabel):
        """
        Sets the labels of the Matplotlib Axes object.
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)


    """
    Private Functions
    """
    def __stars(self,p):

        """
        this is a so called function which can be used in your normal code by
        writing start(data) and as an argument you insert your probabilities.
        it will return a string (a string is a set of characters) which
        contains the stars
        """
        if p < 0.0001:
            return "****"
        elif (p < 0.001):
            return "***"
        elif (p < 0.01):
            return "**"
        elif (p < 0.05):
            return "*"
        else:
            return "-"

    def __hashtags(self,p):
        """
        this is a so called function which can be used in your normal code by
        writing start(data) and as an argument you insert your probabilities.
        it will return a string (a string is a set of characters) which
        contains the stars
        """
        if p < 0.0001:
            return "####"
        elif (p < 0.001):
            return "###"
        elif (p < 0.01):
            return "##"
        elif (p < 0.05):
            return "#"
        else:
            return "-"

    def __set_plot_order(self, dataset_dict):

        #sort according to plot_order
        data = []
        for key in dataset_dict:
            for name in self.plot_order:
                data.append(dataset_dict[key].get(name))
        return data

    def __find_name_position(self, name):
        for group_index, item in enumerate(group_list):
            for index, element in enumerate(item):
                if element == name:
                    first_key_index = (group_index,index)
                    return first_key_index
        else:
            return(None)

    def __significance_labeling_inter_group(self, rects, p_value):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                    hashtags(p_value),
                    ha='center', va='bottom')


#value_label(bar)

    def __set_barchart_value_labels(self, ax, barchart):

        """
        Adds a label of the height of the barchart to the center of the bar.
        :param ax: the matplotlib axes object.
        :param barchart: A bar element.
        """
        for rect in barchart:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height * 0.5, '%0.3f' % height,
                    ha='center', va='bottom')
