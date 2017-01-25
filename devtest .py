from bootstrapit import *
from file_handling import *

analysis_1 = Bootstrapit('flicker.xlsx'               , 
                         number_of_resamples   = 10000 )


export_order_list        = ['Brown' , #First
                            'Green' , 
                            'Blue'  ] #Last
                            
                            
analysis_1.file_export_config( store_data            = False                ,
                               export_file_type      = 'xlsx'                ,
                               export_directory_name = 'bootstrap_results'  ,
                               export_order           = export_order_list   )


#add standard error of the mean to the results
#Works only for get mean at the moment value not for referenced/normalised mean.
analysis_1.use_sem = False

# get mean --------------------------------------------------------------------

data_dict  = analysis_1.get_bootstrapped_mean()
data_dict2 = analysis_1.get_bootstrapped_median() 
data_dict = {'mean'  :data_dict, 
             'median':data_dict2}

#filename_csv = "testfile_csv"
#filename_xls = "testfile_xls"
#filename_xlsx = "testfile_xlsx"

#test csv export
#analysis_1.fh.export_csv(data_dict, export_order_list, filename_csv)
analysis_1.fh.use_directory = True
analysis_1.fh.file_type     = FileType.CSV
analysis_1.fh.export(data_dict)

#test xls export
#analysis_1.fh.export_xls(data_dict, export_order_list, filename_xls)
analysis_1.fh.file_type     = FileType.XLS
analysis_1.fh.export(data_dict)

#test xlsx export
#analysis_1.fh.export_xlsx(data_dict, export_order_list, filename_xlsx)
analysis_1.fh.file_type     = FileType.XLSX
analysis_1.fh.export(data_dict)