import numpy as np
import pandas as pd
import scipy as sp
import scipy.stats as spst
from scipy import stats
import matplotlib.pyplot as plt
import itertools
import csv
import xlrd
import xlwt
#from xlutils.copy import copy #replace with already installed package --> use pandas for import export
import openpyxl
import os
from enum import Enum
import warnings


class FileType(Enum):
    CSV  = "csv"
    XLS  = "xls"
    XLSX = "xlsx"


class FileHandling:
    def __init__(self):
        
        self.directory_name      = 'bootstrapit_results'
        self.file_type           = FileType.XLSX
        self.file_name           = 'bootstrapit_results'      
        self.export_order        = []
        
           
#import methods

    def import_spreadsheet(self, filename):
               
        filetype_check = filename.split('.')
        filetype       = filetype_check[-1]
                 
        if filetype == 'csv':
            dataset_df = pd.read_csv(filename)
        
        elif (filetype == 'xls') or (filetype == 'xlsx'):
            dataset_df = pd.read_excel(filename)
        
        else:
            print ('ERROR: wrong file type')
            return -1
        
        #set data order
        self.export_order = list(dataset_df.columns.values)
        
        #return dataset as dictionary
        return self.__df_to_dict(dataset_df)  

    def __df_to_dict(self, df):
        data_dict = df.to_dict()
        
        #delete pandas dataframe index and nan values from dictionary
        data_dict_reshaped  = {}
        for key in data_dict:
             array = np.array([])
             for index in data_dict[key]:
                  if not np.isnan(data_dict[key][index]):
                      array = np.append(array, data_dict[key][index])
             data_dict_reshaped[key] = array
                                        
        return data_dict_reshaped

    def __column_or_row_ordered(self, row_list):
    
        #if the first row consist of strings, these are probably the headers
        if all(isinstance(n, str) for n in row_list[0]):
            return 'column'
            
        elif all(isinstance(n, str) for n in list(zip(*row_list))[0]):
            return 'row'    
        
        else:
            return 'error'


#export methods 

    def export(self, data_dict):

        if self.file_type  == FileType.CSV :
            print ('csv file export')
            #filename = '_'.join((self.directory_name,function_name))     #what is function name        
            self.__export_csv(data_dict, self.export_order, self.file_name )           
                
        elif self.file_type == FileType.XLS :
            print ('xls file export')
            #filename = '_'.join((self.directory_name,function_name))               
            self.__export_excel(data_dict, self.export_order, self.file_name, "xls") 
                
        elif self.file_type == FileType.XLSX:
            print ('xlsx file export') 
            self.__export_excel(data_dict, self.export_order, self.file_name, "xlsx") 

        else:
            print ('ERROR: unknown export file type')
            return -1
    
    def __export_excel(self, data_dict, order_list, filename, file_ending):
         
        filepath = self.__get_export_filepath(filename, file_ending) 
         
        df = self.__get_export_dataframe(data_dict, order_list)
         
        #export to excel
        writer = pd.ExcelWriter(filepath)
        df.to_excel(writer, sheet_name = "Bootstrapped")
        writer.save()

    def __export_csv(self, data_dict, order_list, filename):
         
         filepath = self.__get_export_filepath(filename, "csv")
         df = self.__get_export_dataframe(data_dict, order_list)
         df.to_csv(filepath)
         
         
    def __get_export_dataframe(self, data_dict, order_list):
        
        #dict to dataframe
        df = pd.DataFrame(data_dict)
         
        #reorder index and return df
        return df.reindex(order_list)
         
         
         
    def __export_csv_old(self, data_dict, order_list, filename):
        
            csv_export_list     = []
            filepath = self.__get_export_filepath(filename, 'csv')
                       
            #start first row with parameters
            export_header = order_list.copy()
            export_header.insert(0, "Parameter")

            #open csv file and write data
            with open(filepath, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow (export_header)

                for parameter, dictionary in data_dict.items():
                    csv_export_list = []
                    csv_export_list.append(parameter)

                    #write dictionaries to list for easier export
                    for name in order_list:
                        csv_export_list.append(dictionary[name])
      
                    #check if there are more than one value in list to export
                    if csv_export_list[1].size > 1:
                        csv_export_list = [list(x) for x in zip(*csv_export_list)]  
                           
                    #write data to file
                    if csv_export_list[1].size > 1:
                        writer.writerows( csv_export_list )
                    else:
                        writer.writerow ( csv_export_list )
                                              

    def __get_export_filepath(self, filename, file_extension):
        #add file type to file name string
        filename = self.__check_filename_for_slashes(filename)
        filename = '.'.join((filename, file_extension))    
            
        #combine filename to a full file path
        self.__create_folder()
        filename = '/'.join((self.directory_name, filename))  

        return filename

    def __check_filename_for_slashes(self, filename):
        filename = filename.replace('/',' ')
        return filename

    def __create_folder(self):  
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)         

    def export_comparison(self, data_dict):
        if self.file_type  == FileType.CSV :
            print ('csv file export')
 
            self.__export_comparison_csv(data_dict, self.export_order, self.file_name )           
                
        elif self.file_type == FileType.XLS :
            print ('xls file export')            
            self.__export_comparison_xls(data_dict, self.export_order, self.file_name )
                
        elif self.file_type == FileType.XLSX:
            print ('xlsx file export')
            self.__export_comparison_xlsx(data_dict, self.export_order, self.file_name) 

        else:
            print ('ERROR: unknown export file type')
            return -1


    #TODO: integrate in general save storage function
    def __export_comparison_csv(self, data_dict, order_list, filename):
        warnings.warn("This functionality is not implemented",RuntimeWarning)
        #filename = self.check_filename_for_slashes(filename)
        #filename = '.'.join((filename,'csv'))     
        #filename = '_'.join((self.directory_name,filename)) 
        #filename = self.check_filename_for_slashes(filename)
        
        #if self.use_directory:
        #    self.__create_folder()
        #    filename = '/'.join((self.directory_name, filename))
    
        
        #export_list = []
        #for key, value in dict.items():
        #    export_list.append([key,value])
        
        
        #with open(filename, 'wb') as f:
        #    dw = csv.writer(f)
        #    dw.writerows(export_list)

    def __export_comparison_xls(self, data_dict, order_list, filename):
        warnings.warn("This functionality is not implemented",RuntimeWarning)
        
        #filename = self.check_filename_for_slashes(filename)
        #filename = '.'.join((filename,'xls'))     
        #filename = '_'.join((self.directory_name,filename)) 
        #filename = self.check_filename_for_slashes(filename)
        
        #if self.use_directory:
        #    self.__create_folder()
        #    filename = '/'.join((self.directory_name, filename))
    
        
        #export_list = []
        #for key, value in dict.items():
        #    export_list.append([key,value])
        
        #worksheetname = self.directory_name
        #worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        #if mode == 'create':        
        #    book  = xlwt.Workbook(encoding="utf-8")
        #    sheet = book.add_sheet(worksheetname)
        #elif mode == 'edit':
        #    rb    = xlrd.open_workbook(filename)
        #    book  = copy(rb)  #TODO: exchange xlutils.copy with another standard anaconda library
        #    sheet = book.get_sheet(0)
        #else:
        #    "Ooops: This xls mode is not known, sorry!!!"            
        
        #for i, l in enumerate(export_list):
        #    for j, col in enumerate(l):
        #        sheet.write(i, j+column_offset, col)
        
        #book.save(filename)


    def __export_comparison_xlsx(self, data_dict, order_list, filename):
        warnings.warn("This functionality is not implemented",RuntimeWarning)

