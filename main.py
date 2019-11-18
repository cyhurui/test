import os
import threading

from readdir import list_all_files, file_txt_name
from readfiles import fileread

__file_in_base = os.path.join(os.getcwd(), "log")
__file_out_base = os.path.join(os.getcwd(), "result")
# __file__read = os.path.join(__file_in_base,"main.txt")

__file_in_base_1 = os.path.join(os.getcwd(), "config")
__file__config = os.path.join(__file_in_base_1, "Config.xlsx")
file_out_temp = os.path.join(__file_out_base, "test_temp.txt")
file_out_final = os.path.join(__file_out_base, "final_file.txt")
if __name__ == "__main__":
    list_all_files()
    dirlist = ["aplogcat-events.txt", "aplogcat-kernel.txt", "aplogcat-radio.txt", "aplogcat-main.txt",
               "aplogcat-system.txt"]
    mutex = threading.Lock()
    fileread(dirlist, file_txt_name(), __file__config)