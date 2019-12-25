import os
import sys
import zipfile
import re
from copy import deepcopy

file_dir = os.path.join(os.getcwd(), "log")


def search(name,file_dir):  # whether this file already exist
    for root, dirs, files in os.walk(file_dir):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1


def unzip_Tree(path):
    if not os.path.exists(path):
        os.makedirs(path)
    for file in os.listdir(path):
        Local = os.path.join(path, file)
        if os.path.isdir(file):
            if not os.path.exists(Local):
                os.makedirs(Local)
            unzip_Tree(path)
        else:
            if os.path.splitext(Local)[1] == '.zip':
                unzip_file(Local)

def unzip_file(file_name):
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name[0:-4]):
        return
        pass
    else:
        os.mkdir(file_name[0:-4])
    for names in zip_file.namelist():
        try:
            zip_file.extract(names, file_name[0:-4])
        except RuntimeError as e:
            print(e)
    zip_file .namelist()
    zip_file .close()
    pass

"""
把所有的目录作为字典的key，对应值为一个list，list里面是带路径的文件名
"""
def list_all_file(file_dir_temp,file_dict):
    split_name =split_path(file_dir_temp,file_dir)
    for root, dirs, files in os.walk(file_dir_temp):
        if len(files) < 1:
            return None

        for file in files:
            if len(os.path.splitext(file)[1]) < 1:
                continue
            if os.path.splitext(file)[1] not in '.txt':
                files.remove(file)
                continue
            else:
                file_dict = merge_list(split_name,file_dict,os.path.join(file_dir_temp,file))
                pass
        return file_dict

def merge_list(split_name,dict,str):
    list = []
    if split_name in dict:
        list = dict[split_name]
        list.append(str)
        dict[split_name] = deepcopy(list)
    else:
        list.append(str)
        dict[split_name] = deepcopy(list)
    list.clear()
    return dict
    pass


def list_all_files(file_dir_temp):
    file_dict ={}
    for dir in os.walk(file_dir_temp):
        #print("------------------")
        #print(dir[0])
        #print(file_dir_temp)
        list_all_file(dir[0],file_dict)
        pass
    #print(file_dict)
    return file_dict



def file_txt_name():
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                # L.append(os.path.join(root, file))
                L.append(file)
    print(L)
    return L


def match(list1, list2):  # check whether requirment file already exit
    ret_list = []
    ret_list = list((set(list1).union(set(list2))) ^ (set(list1) ^ set(list2)))
    print(ret_list)
    return ret_list

def check_include(list1,list2):
    print("########")
    print(list1)
    print(list2)
    list3 = []
    for i in list1:
        for j in list2:
            if i in j:
                list3.append(j)
            else:
                continue
    print(list3)
    return list3
    pass

def changes_file_name(old_file_path, new_file_name):  # 修改文件的名字
    # print(old_file_path)
    # dirname, filename = os.path.split(old_file_path)
    # print(dirname)
    # print(filename)
    # new_file_name = os.path.join(dirname, new_file_name)
    if (check_file_exist(new_file_name)):
        print('new_file_name already exist')
        os.remove(new_file_name)
        os.rename(old_file_path, new_file_name)
    else:
        os.rename(old_file_path, new_file_name)
    return new_file_name
    pass


def check_file_exist(file_path):  # 检查文件是否存在
    if (os.path.exists(file_path)):
        return True
    return False
    pass


def create(dir_path, str_name):  # 根据本地时间创建新文件，如果已存在则不创建,返回新的文件名
    import time
    t = time.strftime('%Y-%m-%d-%H-%M', time.localtime())  # 将指定格式的当前时间以字符串输出
    suffix = ".txt"
    new_file_str = t + str_name + suffix
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    new_file = os.path.join(dir_path, new_file_str)
    print(new_file)
    if not os.path.exists(new_file):
        f = open(new_file, 'w')
        f.close()
        print(new_file + " created.")
    else:
        print(new_file + " already existed.")
    return new_file


def check_excel_file(file_patch):  # 检查后缀是否是excel文件
    if (os.path.exists(file_patch)):
        fname, fename = os.path.splitext(file_patch)
        if "xlsx" in fename:
            return True
    print("Not find config file or the suffixe is not xlsx")
    return False
    pass


def split_path(path,file_in_base):
    sep = '\\'
    altsep = '/'
    path = path.replace(sep,altsep)
    file_in_base=file_in_base.replace(sep,altsep)
    name = path[len(file_in_base):]
    if len(name) < 1:
        name =["log"]
    if altsep in name:
        name = name.split(altsep)
        name = list(filter(None,name))
    return name[0]


# file_name(file_dir)
# list_all_files()
# file_txt_name()
# match([1, 2, 3],[3, 0, 2])
# print(os.path.abspath('host.txt'))
#file = "aplogcat-kernel.txt"
#unzip_Tree(file_dir)
#file_txt_name()
#search("aplogcat-kernel.txt")
#print(list_all_files(file_dir))
#__file_in_base = os.path.join(os.getcwd(), "log")
#path = " 'D:\\program files (x86)\\python\\project\\test\\log\\NDFL2D0041_308011361_USER@2019-11-15_21_47_51_-0300_IKUT-1366581\\wlan_logs\\host_driver_logs_current.txt"
#print(os.path.basename(path))
#print(path)
#split_path(path,__file_in_base)

#file_txt_name()
