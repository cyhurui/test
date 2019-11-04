import os

file_dir = os.path.join(os.getcwd(), "log/")


def search(name):  # whether this file already exist
    for root, dirs, files in os.walk(file_dir):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1


def list_all_files():
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        return files


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


def changes_file_name(old_file_path, new_file_name):  # 修改文件的名字
    # print(old_file_path)
    #dirname, filename = os.path.split(old_file_path)
    # print(dirname)
    # print(filename)
    #new_file_name = os.path.join(dirname, new_file_name)
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

# file_name(file_dir)
# list_all_files()
# file_txt_name()
# match([1, 2, 3],[3, 0, 2])
# print(os.path.abspath('host.txt'))
