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
        
        self.use_directory       = True
        self.use_file            = True
        self.directory_name      = 'bootstrapit_results'
        self.file_type           = FileType.XLSX
        self.file_name           = 'bootstrapit_results'      
        self.export_order        = []
        
           
#import methods

    def import_spreadsheet(self, filename):
               
        filetype_check = filename.split('.')
        filetype       = filetype_check[-1]

        
                   
        if filetype == 'csv':
            row_list = self.__parse_csv(filename)
        
        elif (filetype == 'xls') or (filetype == 'xlsx'):
            row_list = self.__parse_xls_xlsx(filename)
        
        else:
            print ('ERROR: wrong file type')
            return -1

        if self.__column_or_row_ordered(row_list) == 'error':
            print ('ERROR: something is wrong with your spreadsheet layout')
            return -1
        
        elif self.__column_or_row_ordered(row_list) == 'row':
            transposed_list = [list(x) for x in zip(*row_list)]        
            list_order      = transposed_list[0]
        
        elif self.__column_or_row_ordered(row_list) == 'column':
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
                warnings.warn('Dataset contains empty cells, if this is ok go on', RuntimeWarning)
                for item in value:
                    #just add the elements which are not empty                
                    if item:                
                        data_array = np.append(data_array, item)
                        
                new_dataset[key] = data_array
        
        #return dataset as dictionary and list order as list
        return new_dataset, list_order  

    def __column_or_row_ordered(self, row_list):
    
        #if the first row consist of strings, these are probably the headers
        if all(isinstance(n, str) for n in row_list[0]):
            return 'column'
            
        elif all(isinstance(n, str) for n in list(zip(*row_list))[0]):
            return 'row'    
        
        else:
            return 'error'

    def __parse_xls_xlsx(self, filename):
    
        book  = xlrd.open_workbook(filename)
        sheet = book.sheet_by_index(0)
        
        row_list = []
        for row_ind in range(sheet.nrows):
            row_values = sheet.row_values(row_ind)
            row_list.append(row_values)
        
        return row_list

    def __parse_csv(self, filename):
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


#export methods 

    def export(self, data_dict):

        if self.file_type  == FileType.CSV :
            print ('csv file export')
            #filename = '_'.join((self.directory_name,function_name))     #what is function name        
            self.__export_csv(data_dict, self.export_order, self.file_name )           
                
        elif self.file_type == FileType.XLS :
            print ('xls file export')
            #filename = '_'.join((self.directory_name,function_name))               
            self.__export_xls(data_dict, self.export_order, self.file_name )
                
        elif self.file_type == FileType.XLSX:
            print ('xlsx file export')
            #filename = '_'.join((self.directory_name,function_name)) 
            self.__export_xlsx(data_dict, self.export_order, self.file_name) 

        else:
            print ('ERROR: unknown export file type')
            return -1

    def __export_csv(self, data_dict, order_list, filename):
        
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
                                              
    def __export_xls(self, data_dict, order_list , filename):
    
        xls_export_list     = []
        filepath = self.__get_export_filepath(filename, 'xls')
                       
        #start first row with parameters
        export_header = order_list.copy()
        export_header.insert(0, "Parameter")

        #open xls file and write data
        worksheetname = self.directory_name
        worksheetname = self.__check_filename_for_slashes(worksheetname)    
        
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet(worksheetname)
        excell_list = []
        excell_list.append(export_header)


        for parameter, dictionary in data_dict.items():
            xls_export_list = []
            xls_export_list.append(parameter)

            #write dictionaries to list for easier export
            for name in order_list:
                xls_export_list.append(dictionary[name])
      
            #check if there are more than one value in list to export
            if xls_export_list[1].size > 1:
                xls_export_list = [list(x) for x in zip(*xls_export_list)] 
    
            excell_list.append(xls_export_list)
 
        for i, l in enumerate(excell_list):
            for j, col in enumerate(l):
                sheet.write(i, j, col)
        
        book.save(filepath)
    
    def __export_xlsx(self, data_dict, order_list , filename):
    
            xlsx_export_list     = []
            filepath = self.__get_export_filepath(filename, 'xlsx')
                       
            #start first row with parameters
            export_header = order_list.copy()
            export_header.insert(0, "Parameter")

            #open xlsx file and write data
            worksheetname = self.directory_name
            worksheetname = self.__check_filename_for_slashes(worksheetname)    
        
            #create xlsx workbook
            book        = openpyxl.Workbook(encoding="utf-8")
            sheet       = book.active
            sheet.title = worksheetname

            #initalise header parameter
            excell_list = []
            excell_list.append(export_header)


            for parameter, dictionary in data_dict.items():
                xls_export_list = []
                xls_export_list.append(parameter)

                #write dictionaries to list for easier export
                for name in order_list:
                    xls_export_list.append(dictionary[name])
      
                #check if there are more than one value in list to export
                if xls_export_list[1].size > 1:
                    xls_export_list = [list(x) for x in zip(*xls_export_list)] 
    
                excell_list.append(xls_export_list)
 
            for i, l in enumerate(excell_list):
                for col, value in enumerate(l):
                    sheet.cell(row=i+1, column=col+1).value = value
                    
                            
            book.save(filepath)

    def __get_export_filepath(self, filename, file_extension):
        #add file type to file name string
        filename = self.__check_filename_for_slashes(filename)
        filename = '.'.join((filename, file_extension))    
            
        #combine filename to a full file path
        if self.use_directory:
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

