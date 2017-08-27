import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#==============================================================================
# plotting FIXME: Just sketching the functionality has to be changed for
#                 a nicer API
#==============================================================================



SPACE = ' '

def stars(p):
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

def hashtags(p):
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



def plot_barchart(dataset_dict, plot_order, title = '', xlabel = '', ylabel = ''):
    """
    Barchart plots the input dataset dictionary according to the key order in 
    the input plot_order variable. It also plots the value of the specific key
    above the center of the corresponding bar.
    """
    
    #sort according to plot_order
    data = []
    for key in dataset_dict:
          
        for name in plot_order:
            data.append(dataset_dict[key].get(name))  
        
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)

    #plot barchart
    barchart = ax.bar( range( len(plot_order) ), data, align = 'center')#, color=my_colors)
    
    # TODO: alignment looks to irregular, search for different solution
    plt.xticks( range( len(plot_order) ) , plot_order, rotation = 45)
    
    #set axis labels
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    
    #add value label to each bar   
    for rect in barchart:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height * 0.5 ,
            '%0.3f' % height,
            ha='center', va='bottom')
    
    plt.show()
    
    
    
def plot_barchart_experimental(dataset          , 
                               plot_order       , 
                               comparisons = [] , #used for significance
                               reference = ''   , 
                               xlabel = ''      , 
                               ylabel = ''      ):
    """
    Barchart plots the input dataset dictionary according to the key order in 
    the input plot_order variable. It also plots the value of the specific key
    above the center of the corresponding bar.
    """
    
    #sort according to plot_order
    data = []
    for name in plot_order:
        data.append(dataset.get(name))  
        
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)

    #plot barchart
    barchart = ax.bar( range( len(dataset) ), data, align = 'center', color=my_colors)
    
    # TODO: alignment looks to irregular, search for different solution
    plt.xticks( range( len(dataset) ) , plot_order, rotation = 45)
    
    #set axis labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    #add value label to each bar   
    for rect in barchart:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height * 0.5 ,
            '%0.3f' % height,
            ha='center', va='bottom')    

    
    #take the comparison statistic
    
    
    
    
    
    
    
    
    

#this is only for experimental trials and not functional   
def plot_barchart_sign(dataset, significance_dataset, plot_order):
    
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
    
  




def find_name_position(name):
    for group_index, item in enumerate(group_list):
        for index, element in enumerate(item):
            if element == name:
                first_key_index = (group_index,index)
                return first_key_index
    else:
        return(None)
    


def significance_labeling_inter_group(rects, p_value):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                hashtags(p_value),
                ha='center', va='bottom')


#value_label(bar)