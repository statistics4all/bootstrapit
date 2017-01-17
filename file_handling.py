import numpy as np
import scipy as sp
import scipy.stats as spst
from scipy import stats
import matplotlib.pyplot as plt
import itertools
import csv
import xlrd
import xlwt
from xlutils.copy import copy #replace with already installed package
import os
from enum import Enum


class FileType(Enum):
    CSV  = "csv"
    XLS  = "xls"
    XLSX = "xlsx"


class FileHandling:
    def __init__(self):
        
        self.use_directory       = False
        self.use_file            = False
        self. directory_name     = 'bootstrapit_results'
        self.file_type           = FileType.XLSX
        self.file_name           = 'bootstrapit_results'      
        self.export_order        = []
        
            
    def create_folder(self):
        #TODO: add gui prompt to choose directory    
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)    


#import methods

    def import_spreadsheet(self, filename):
               
        filetype_check = filename.split('.')
        filetype       = filetype_check[-1]
                   
        if filetype == 'csv':
            #call function parse csv
            row_list = self.parse_csv(filename)
        
        elif (filetype == 'xls') or (filetype == 'xlsx'):
            #call function pass xls
            row_list = self.parse_xls_xlsx(filename)
        
        else:
            print ('ERROR: wrong file type')
            return -1
    
        if self.column_or_row_ordered(row_list) == 'error':
            print ('ERROR: something is wrong with your spreadsheet layout')
            return -1
        
        elif self.column_or_row_ordered(row_list) == 'row':
            transposed_list = [list(x) for x in zip(*row_list)]        
            list_order      = transposed_list[0]
        
        elif self.column_or_row_ordered(row_list) == 'column':
            #transpose the lists
            list_order  = row_list[0]          
            row_list    = [list(x) for x in zip(*row_list)]
               
        else:
            print ('ERROR: something is wrong with your spreadsheet layout')
            return -1
            
        
        #change list to dictionary with first row as keys        
        datasets = {}
        for column in row_list:
            datasets[column[0]] = column[1:]
    
        new_dataset = {}
        for key, value in datasets.items():
            
            #try to convert list to numpy float array        
            try:
                new_dataset[key] =  np.asarray(value, dtype=np.float)
            
            #when this fails there is possbily a empty cell
            except ValueError:
                data_array = np.array([], dtype = np.float)
                print ('Dataset contains empty cells, if this is ok go on')
                for item in value:
                    #just add the elements which are not empty                
                    if item:                
                        data_array = np.append(data_array, item)
                        
                new_dataset[key] = data_array
        
        #return dataset as dictionary and list order as list
        return new_dataset, list_order  


    def column_or_row_ordered(self, row_list):
    
        #if the first row consist of strings, these are probably the headers
        if all(isinstance(n, str) for n in row_list[0]):
            return 'column'
            
        elif all(isinstance(n, str) for n in list(zip(*row_list))[0]):
            return 'row'    
        
        else:
            return 'error'


    def parse_xls_xlsx(self, filename):
    
        book  = xlrd.open_workbook(filename)
        sheet = book.sheet_by_index(0)
        
        row_list = []
        for row_ind in range(sheet.nrows):
            row_values = sheet.row_values(row_ind)
            row_list.append(row_values)
        
        return row_list


    def parse_csv(self, filename):
        with open(filename) as csvfile:
                
                #check what delimiters the file uses
                dialect = csv.Sniffer().sniff( csvfile.read(1024) )
                
                #seek to the beginning of the file
                csvfile.seek(0)
                
                #read all rows and append them to a list  
                reader = csv.reader(csvfile,dialect)
                row_list = []
                for row in reader:
                    row_list.append(row)
                
        return row_list

#-----------------------------------------------------------------------------------------------------

#export methods
# 1. get dictionary containing dictionaries.
# 2. check export file extension.
# 3. export dictionaries as rows with key as row name in the first column.

    def export(self, data_dict):

        if self.file_type  == 'csv' :
            print ('csv file export')
            filename = '_'.join((self.directory_name,function_name))              
            self.export_csv(data_dict, self.export_order, filename)           
                
        elif self.file_type == 'xls' :
            print ('xls file export')
            filename = '_'.join((self.directory_name,function_name))               
            self.export_xls(data_dict, self.export_order, filename)
                
        elif self.file_type == 'xlsx':
            print ('xlsx file export')
            self.export_xlsx(data_dict, self.export_order, filename) 

        else:
            print ('ERROR: unknown export file type')
            return -1



    def __get_export_filepath(self, filename, file_extension):
        #add file type to file name string
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename, file_extension))    
            
        #combine filename to a full file path
        if self.use_directory:
             self.create_folder()
             filename = '/'.join((self.directory_name, filename))  

        return filename
     

    def export_csv(self, data_dict, order_list, filename):
        
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
                     
                               
        
    def export_xls(self       , 
                         data_dict  , 
                         order_list , 
                         filename  ):
    
        csv_export_list     = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls'))    
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            
    
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
        excell_list = []
        excell_list.append(order_list)
        excell_list.append(csv_export_list)
 
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        for i, l in enumerate(excell_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filename)
















    def save_dictionary_to_csv(self, dict, order_list, filename):
           
        for parameter, dictionary in self.dict.items():
            csv_export_list = []

            #write dictionaries to list for easier export
            for name in order_list:
                csv_export_list.append(dictionary[name])
      
            #check if there are more than one value in list to export
            if csv_export_list[0].size > 1:
                csv_export_list = [list(x) for x in zip(*csv_export_list)]  
        
            with open(filename, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow (order_list)
            
                if csv_export_list[0].size > 1:
                    writer.writerows( csv_export_list )
                else:
                    writer.writerow ( csv_export_list )





    
    def check_filename_for_slashes(self, filename):
        filename = filename.replace('/',' ')
        return filename

            
            
    def save_data_with_sem_to_csv(self       , 
                                  data_dict  , 
                                  sem_dict   , 
                                  order_list , 
                                  filename  ):
    
        csv_export_list     = []
        csv_sem_export_list = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'csv'))    
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            csv_sem_export_list.append( sem_dict[name]  )
            
    
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
    
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow ( order_list )
            
            if csv_export_list[0].size > 1:
                writer.writerows( csv_export_list )
            else:
                writer.writerow ( csv_export_list )
            
            writer.writerow(csv_sem_export_list)
        
        
    def save_data_with_sem_to_xls(self , 
                                  data_dict  , 
                                  sem_dict   , 
                                  order_list , 
                                  filename  ):
    
        csv_export_list     = []
        csv_sem_export_list = []
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls')) 
        
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))    
        
        for name in order_list:
            csv_export_list.append    ( data_dict[name] )
            csv_sem_export_list.append( sem_dict[name]  )
        
        #check if there are more than one value in list to export
        if csv_export_list[0].size > 1:
            csv_export_list = [list(x) for x in zip(*csv_export_list)]  
    
        excell_list = []
        excell_list.append(order_list)
        excell_list.append(csv_export_list)
        excell_list.append(csv_sem_export_list)
        
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        for i, l in enumerate(excell_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filename)
    





    #TODO: integrate in general save storage function
    def save_unordered_dictionary_to_csv(self, dict, filename):
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'csv'))     
        filename = '_'.join((self.directory_name,filename)) 
        filename = self.check_filename_for_slashes(filename)
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))
    
        
        export_list = []
        for key, value in dict.items():
            export_list.append([key,value])
        
        
        with open(filename, 'wb') as f:
            dw = csv.writer(f)
            dw.writerows(export_list)

    def save_unordered_dictionary_to_xls(self, dict, filename, mode = 'create',column_offset = 0):
        
        filename = self.check_filename_for_slashes(filename)
        filename = '.'.join((filename,'xls'))     
        filename = '_'.join((self.directory_name,filename)) 
        filename = self.check_filename_for_slashes(filename)
        
        if self.use_directory:
            self.create_folder()
            filename = '/'.join((self.directory_name, filename))
    
        
        export_list = []
        for key, value in dict.items():
            export_list.append([key,value])
        
        worksheetname = self.directory_name
        worksheetname = self.check_filename_for_slashes(worksheetname)    
        
        if mode == 'create':        
            book  = xlwt.Workbook(encoding="utf-8")
            sheet = book.add_sheet(worksheetname)
        elif mode == 'edit':
            rb    = xlrd.open_workbook(filename)
            book  = copy(rb)  #TODO: exchange xlutils.copy with another standard anaconda library
            sheet = book.get_sheet(0)
        else:
            "Ooops: This xls mode is not known, sorry!!!"            
        
        for i, l in enumerate(export_list):
            for j, col in enumerate(l):
                sheet.write(i, j+column_offset, col)
        
        book.save(filename)

