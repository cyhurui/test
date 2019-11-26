import datetime
import os
import shutil
import time
from datetime import date, datetime

DBG = False
debug_DBG =True
tag = "readfiles"

# lines_list_1 =[]
# lines_list_2 =[]
from readdir import changes_file_name, check_file_exist, create


def log(tag, logstr):
    if (DBG):
        print(str(datetime.now()) + "  " + tag + ":" + str(logstr))
        # print()
    pass


def log_debug(logstr):
    if debug_DBG:
        print(str(datetime.now()) + ":   " + str(logstr))
    pass


def merge_log(__file_read_1, __file_read_2, __file_out, mdelete):  # 按照时间顺序合并成最终的log文件,log 文件名为最后一个文件名，并且可以删除合并的原始文件
    log_debug("merge log: file1:" + __file_read_1 + "--file2:" + __file_read_2 + "---outfile:" + __file_out)
    #re-create out file
    delete_file(__file_out)
    if check_file_exist(__file_out) is not True:
        file_out = open(__file_out, 'w')
        file_out.close()
        pass

    if check_file_exist(__file_read_1) is not True:
        file_out = open(__file_read_1, 'w')
        file_out.close()
        pass

    if not check_file_exist(__file_read_2):
        return
        pass
    with open(__file_read_1, 'r', encoding="UTF-8") as file_read_1:
        #print("----------------")
        file_read_2 = open(__file_read_2, 'r', encoding="UTF-8")
        file_out = open(__file_out, 'w', encoding="UTF-8")
        lines_list_1 = None
        lines_list_2 = None
        while True:
            if lines_list_1 is None:
                lines_1 = file_read_1.readline()  # 整行读取数据
                log(tag,lines_1)
                lines_list_1 = lines_1

            if lines_list_2 is None:
                lines_2 = file_read_2.readline()
                log(tag,lines_2)
                lines_list_2 = lines_2
                # print("main.txt ；"+lines_list_2)
            if not lines_1:
                if lines_list_1 is not -1:
                    #print("file:" + file_read_1.name + " is finish")
                    lines_list_1 = -1
                    lines_1 = -1
                    file_read_1.close()

            if not lines_2:
                if lines_list_2 is not -1:
                    #print("file:" + file_read_2.name + " is finish")
                    lines_list_2 = -1
                    lines_2 = -1
                    file_read_2.close()

            if (lines_list_2 == -1 and lines_list_1 == -1):
                break
            elif (lines_list_2 == -1):
                #print(str_addition(lines_1,"-->" +intercept_file_name(__file_read_1)))
                if "test_temp" in intercept_file_name(__file_read_1):
                    file_out.write(lines_1)
                else:
                    file_out.write(str_addition(lines_1, "-->" + intercept_file_name(__file_read_1)))
                #lines_list_1 = -1
                lines_list_1 = None
                continue
            elif lines_list_1 == -1:
                #print(str_addition(lines_2,'-->'+intercept_file_name(__file_read_2)))
                if "test_temp" in intercept_file_name(__file_read_2):
                    file_out.write(lines_2)
                else:
                    file_out.write(str_addition(lines_2, '-->' + intercept_file_name(__file_read_2)))
                #file_out.write(lines_2)
                #lines_list_2 = -1
                lines_list_2 = None
                continue
            """
            compare lines1 and lines 2 date and Rearrange
            """
            lines_1_date = outputdate(lines_list_1)
            lines_2_date = outputdate(lines_list_2)

            if (lines_1_date == -1 or lines_1_date == -2):
                if isinstance(lines_1, str):
                    #print(str_addition(lines_1, '-->'+intercept_file_name(__file_read_1)))
                    # print(str_addition(lines_1,"-->" +intercept_file_name(__file_read_1)))
                    if "test_temp" in intercept_file_name(__file_read_1):
                        file_out.write(lines_1)
                    else:
                        file_out.write(str_addition(lines_1, "-->" + intercept_file_name(__file_read_1)))
                    #file_out.write(lines_1)
                    lines_list_1 = None
                    log(tag,"lines_1_date is -1 or -2")
                continue

            if (lines_2_date == -1 or lines_2_date == -2):
                if isinstance(lines_1, str):
                    log(tag,"lines_2_date is -1 or lines_list_1 is -1)")
                    #print(str_addition(lines_2, '-->'+intercept_file_name(__file_read_2)))
                    if "test_temp" in intercept_file_name(__file_read_2):
                        file_out.write(lines_2)
                    else:
                        file_out.write(str_addition(lines_2, '-->' + intercept_file_name(__file_read_2)))
                    #file_out.write(lines_2)
                    lines_list_2 = None
                    log(tag,"lines_2_date is -1 or -2")
                continue
            if (compare(lines_1_date, lines_2_date)):
                #print(str_addition(lines_1,'-->'+ intercept_file_name(__file_read_1)))
                if "test_temp" in intercept_file_name(__file_read_1):
                    file_out.write(lines_1)
                else:
                    file_out.write(str_addition(lines_1, "-->" + intercept_file_name(__file_read_1)))
                #file_out.write(lines_1)
                lines_list_1 = None
                continue
            else:
                #print(str_addition(lines_2,'-->'+intercept_file_name(__file_read_2)))
                if "test_temp" in intercept_file_name(__file_read_2):
                    file_out.write(lines_2)
                else:
                    file_out.write(str_addition(lines_2, '-->' + intercept_file_name(__file_read_2)))
                #file_out.write(lines_2)
                lines_list_2 = None
                continue
    file_read_1.close()
    file_read_2.close()
    file_out.close()

    if (check_file_exist(__file_out)):
        delete_file(__file_read_2)
        delete_file(__file_read_1)
        if mdelete is True:
            changes_file_name( __file_out,__file_read_1)
            log_debug("Temporary files merged successfully")
        else:
            log_debug("Merged successfully")
    else:
        log_debug("Output file does not exist")


def str_addition(mstr,suffix):
    return mstr.replace('\r',' ').replace('\n',' ').replace('\t',' ')+suffix+"\n"


def checkFileSize(filePath):
    fsize = os.path.getsize(filePath)
    if fsize <= 1:
        delete_file(filePath)
        log_debug(filePath)
        log_debug("the size is 0 and delete it")
        return False
    return True
    pass


def SortedFile(file, out_file):
    print("Sorted:"+file)
    list = []
    with open(file, 'r',encoding="UTF-8") as f:
        for line in f:
            list.append(line.strip())

    with open(out_file, "w",encoding="UTF-8") as f:
        for item in sorted(list):
            f.writelines(item)
            f.writelines('\n')
        f.close()


def delete_file(file):
    print("delete file:" + file)
    dirPath = os.path.join(os.getcwd(), "result")
    if (os.path.exists(file)):
        os.remove(file)
        #print('移除后test 目录下有文件：%s' % os.listdir(dirPath))
    else:
        #print("要删除的文件不存在！")
        pass


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
            if ">" not in strlist:
                print("it don't need compare")
                return -1
            strlist = str_temp.split("-->")
            print("-------1111--------")
            print(strlist[1])
            print("--------2222-------")
            return outputdate(strlist[1])
    else:
        # print(str_temp)
        return -2

    pass


def compare(date_1, date_2):
    return date_1 <= date_2
    pass


def intercept_file_name(file):  # file 必须为完整路径,取完整路径的文件名，比如：aplogcat-kernel.txt 取aplogcat-kernel
    # print("intercept_file_name: file")
    # print(file)
    file_temp = os.path.basename(str(file))
    # str_temp = str(file.name)
    index = file_temp.split(".")
    # str_temp = str.split("/")
    # return "123"
    return index[0]
    # return str_temp[-1]


__file_in_base = os.path.join(os.getcwd(), "log")
__file_out_base = os.path.join(os.getcwd(), "result")
# __file__read = os.path.join(__file_in_base,"main.txt")
__file__config = os.path.join(__file_in_base, "Config.xlsx")
__file__out = os.path.join(__file_out_base, "test.txt")

file1 = os.path.join(__file_out_base, "aplogcat-events.txt")
file2 = os.path.join(__file_out_base, "aplogcat-main.txt")
file5 = os.path.join(__file_out_base, "aplogcat-kernel.txt")
file3 = os.path.join(__file_out_base, "test_temp.txt")
file6 = os.path.join(__file_out_base, "final_file.txt")
file4 = []
# __file__out = create(__file_out_base, intercept_file_name(file1))
file4.append(file3)
file4.append(file1)
file4.append(file2)
file4.append(file5)
"""

if len(file4) >= 2:
    while (1):
        if len(file4) < 2:
            break
            pass
        elif len(file4) == 2:
            merge_log(file4[0], file4[1], file6, False)
            file4.remove(file4[1])
            pass
        else:
            merge_log(file4[0], file4[1], file6, True)
            file4.remove(file4[1])
            pass
        pass
    pass
pass


a = "aaaaaaaaaaaaaaaaaaaaaaa"
b ="bbb"
c= a+b
#print(a+'-->'+b)

# print(os.path.basename(file1))
# merge_log(file4[0],file4[1],file4[2],True)
# SortedFile(file1,file1)
# print(intercept_file_name(file4[0]))
# merge_log(file1,file2,file3)
#changes_file_name(file1,file3)
"""