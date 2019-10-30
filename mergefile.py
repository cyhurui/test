import os
import time


# lines_list_1 =[]
# lines_list_2 =[]
from readdir import changes_file_name, check_file_exist


def merge_log(file_read_1, file_read_2, file_out,mdelete):  # 按照时间顺序合并成最终的log文件,log 文件名为最后一个文件名，并且可以删除合并的原始文件
    print("merge log: file1:"+file_read_1+"--file2:"+file_read_2+"outfile:"+file_out+"--delete:"+mdelete)
    with open(file_read_1, 'r', encoding="UTF-8") as file_read_1:
        print("----------------")
        file_read_2 = open(file_read_2, 'r', encoding="UTF-8")
        file_out = open(file_out, 'w', encoding="UTF-8")
        lines_list_1 = None
        lines_list_2 = None
        while True:
            if lines_list_1 is None:
                lines_1 = file_read_1.readline()  # 整行读取数据
                lines_list_1 = lines_1

            if lines_list_2 is None:
                lines_2 = file_read_2.readline()
                lines_list_2 = lines_2
                # print("main.txt ；"+lines_list_2)

            if not lines_1:
                if lines_list_1 is not -1:
                    print("file:" + file_read_1.name + " is finish")
                    lines_list_1 = -1
                    lines_1 = -1
                    file_read_1.close()

            if not lines_2:
                if lines_list_2 is not -1:
                    print("file:" + file_read_2.name + " is finish")
                    lines_list_2 = -1
                    lines_2 = -1
                    file_read_2.close()

            if (lines_list_2 == -1 and lines_list_1 == -1):
                break
            elif (lines_list_2 == -1):
                file_out.write(intercept_file_name(file_read_1) + "-->" + lines_1)
                lines_list_1 = -1
            elif lines_list_1 == -1:
                file_out.write(intercept_file_name(file_read_2) + "-->" + lines_2)
                lines_list_2 = -1

            lines_1_date = outputdate(lines_list_1)
            lines_2_date = outputdate(lines_list_2)

            if (lines_1_date == -1 or lines_1_date == -2):
                if isinstance(lines_1, str):
                    file_out.write(intercept_file_name(file_read_1) + "-->" + lines_1)
                    lines_list_1 = None
                    print("lines_1_date == -1 or -2")
                continue

            if (lines_2_date == -1 or lines_2_date == -2):
                if isinstance(lines_1, str):
                    print("lines_2_date == -1 or lines_list_1 == -1)")
                    file_out.write(intercept_file_name(file_read_2) + "-->" + lines_2)
                    lines_list_2 = None
                    print("lines_2_date == -1 or -2")
                continue
            if (compare(lines_1_date, lines_2_date)):
                file_out.write(intercept_file_name(file_read_1) + "-->" + lines_1)
                lines_list_1 = None
            else:
                file_out.write(intercept_file_name(file_read_2) + "-->" + lines_2)
                lines_list_2 = None
        file_read_1.close()
        file_read_2.close()
        file_out.close
        if (check_file_exist(file_out) & mdelete):
            delete_file(file_read_2)
            delete_file(file_read_1)
            changes_file_name(file_out, file_read_2)

            # print(a)


def delete_file(file):
    print("delete file:"+file)
    dirPath = os.path.join(os.getcwd(), "result")
    if (os.path.exists(file)):
        os.remove(file)
        print('移除后test 目录下有文件：%s' % os.listdir(dirPath))
    else:
        print ("要删除的文件不存在！")


def is_valid_date(str):
    try:
        if ":" in str:
            # print("debug:" + str)
            time.strptime(str, "%m-%d %H:%M:%S.%f")
            return True
        else:
            print("not find date in this line")
            return False
    except:
        print("it has exception")
        return False


# def is_valid_date(str):
# '''判断是否是一个有效的日期字符串'''
# try:
# time.strptime(str, "%m-%d %H:%M:%S:%f")
# return True
# except:
# return False###

def outputdate(str_temp):
    if isinstance(str_temp, str):
        strlist = str_temp.split()
        # print(strlist)
        if (len(strlist) < 2):
            return -2
        str_temp = strlist[0] + " " + strlist[1]
        if (is_valid_date(str_temp)):
            s_time = time.strptime(str_temp, "%m-%d %H:%M:%S.%f")
            return s_time
        else:
            return -1
    else:
        # print(str_temp)
        return -2

    pass


def compare(date_1, date_2):
    return date_1 <= date_2
    pass


def intercept_file_name(file):  #file 必须为完整路径,取完整路径的文件名，比如：aplogcat-kernel.txt 取aplogcat-kernel
    #print("intercept_file_name: file")
    #print(file)
    file_temp = os.path.basename(file)
    # str_temp = str(file.name)
    index = file_temp.split(".")
    # str_temp = str.split("/")
    # return str_temp
    return index[0]
    # return str_temp[-1]


__file_in_base = os.path.join(os.getcwd(), "log")
__file_out_base = os.path.join(os.getcwd(), "result")
# __file__read = os.path.join(__file_in_base,"main.txt")
__file__config = os.path.join(__file_in_base, "Config.xlsx")
__file__out = os.path.join(__file_out_base, "test.txt")

file1 = os.path.join(__file_in_base, "aplogcat-kernel.txt")
file2 = os.path.join(__file_in_base, "aplogcat-main.txt")
file3 = os.path.join(__file_out_base, "test.txt")

print(os.path.basename(file1))
print(intercept_file_name(file1))


# merge_log(file1,file2,file3)
