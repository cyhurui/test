import os

from readdir import list_all_files, file_txt_name, unzip_Tree
from readfiles import fileread
from readconfig import get_all_sheet_name, filter_valid_sheet

__file_in_base = os.path.join(os.getcwd(), "log")
__file_out_base = os.path.join(os.getcwd(), "result")
# __file__read = os.path.join(__file_in_base,"main.txt")

__file_in_base_1 = os.path.join(os.getcwd(), "config")
__file__config = os.path.join(__file_in_base_1, "Config.xlsx")
file_out_temp = os.path.join(__file_out_base, "test_temp.txt")
file_out_final = os.path.join(__file_out_base, "final_file.txt")

if __name__ == "__main__":
    unzip_Tree(__file_in_base)
    """
    all_file_dict的格式字典，其中key是bug2go解压之后的文件，对应的值是一个全路径的文件名
    {'log': ['D:\\program files (x86)\\python\\project\\test\\log\\aplogcat-crash.txt'], 
    'NDFL2D0041_308011361_USER@2019-11-15_21_47_51_-0300_IKUT-1366581': ['D:\\program files (x86)\\python\\project\\test\\log\\NDFL2D0041_308011361_USER@2019-11-15_21_47_51_-0300_IKUT-1366581\\aplogcat-crash.txt'],
    'NDFL2G0016_307712978_USER@2019-10-16_23_36_40_-0300_IKUT-1357018': ['D:\\program files (x86)\\python\\project\\test\\log\\NDFL2G0016_307712978_USER@2019-10-16_23_36_40_-0300_IKUT-1357018\\aplogcat-crash.txt']
    """
    all_file_dict = list_all_files(__file_in_base)
    dirlist = ["aplogcat-events.txt", "aplogcat-kernel.txt", "aplogcat-radio.txt", "aplogcat-main.txt",
               "aplogcat-system.txt","host_driver_logs_current.txt"]
    #fileread(dirlist, file_txt_name(), __file__config)
    sheet_name = get_all_sheet_name(__file__config)
    sheet_name_dict = filter_valid_sheet(__file__config, False)
    for key in all_file_dict.keys():
        file_out_base = os.path.join(__file_out_base,key)
        fileread(dirlist, all_file_dict[key], __file__config,__file_in_base,file_out_base,sheet_name,sheet_name_dict)