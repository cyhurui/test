import os
import re
import sys
from concurrent.futures import thread
from copy import deepcopy
from typing import List, Any, Dict
import threading

from mergefile import intercept_file_name, merge_log, SortedFile, checkFileSize
from readdir import list_all_files, check_excel_file, changes_file_name, create, check_file_exist
from readdir import file_txt_name
from readdir import match
from readconfig import read_excel, get_all_sheet_name, get_all_config, get_tag, find_tag
from readconfig import excel_cols

import xlrd
from datetime import date, datetime

dict = {}
pos: List[Any] = []
arg = ''
readinlist = []
merge_file_list = []
DBG = False
debug_DBG = False

Tag = "readfile"

exitFlag = 0
threadLock = threading.Lock()
threads = []
threadID = 1


def log(tag, logstr):
    if (DBG):
        print(str(datetime.now()) + "  " + tag + ":" + str(logstr))
        # print()
    pass

def log_debug(logstr):
    if debug_DBG:
        print(str(datetime.now()) + ":   " + str(logstr))
        print()
    pass

def write_file(param, f_output, f_input):
    log(Tag, "*********")
    log(Tag, f_input)
    # file_name = intercept_file_name(f_input)
    if param is '':
        pass
    else:
        log(Tag, param)
        log(Tag, f_output)
        f_output.write(param + "\n")
    pass


# 在这个判断中，config中必须包含MANDATORY这个key，如果value_flag字段在config中没有，说明没有val值和逻辑单元
def decode_Logic_config(str_line, config, key, tag_temp, sheet_name_temp):
    list_temp = tag_temp[sheet_name_temp]
    value_str = []
    mandatory_index = find_tag(list_temp, "MANDATORY")
    if mandatory_index == -1:
        print("in config file, it has no MANDATORY")
        return -1

    value_flag_index = find_tag(list_temp, "VALUE_FLAG")
    if value_flag_index == -1:
        return 1  # 这个表明在这个列表中不需要val和逻辑单元的判断

    logic_unit_index = find_tag(list_temp, 'LOGIC UNIT')
    if logic_unit_index == -1:
        print("logic unit is non-exist in config")

    val_dic: Dict[Any, Any] = {}
    for j in list_temp:  # 这个是为了把Val值取出来
        if "VALUE_FLAG" == j:
            continue
        if "VAL" in j:
            if config[key][value_flag_index] == 0:
                print("the value flag set to 0,don't need to read value")
                return 1
            val_index = find_tag(list_temp, j)
            if val_index == -1:
                print("in this config, it has no VAL1")
                return 1
            value_str.append(val_index)
            val_dic[key + "_" + j] = config[key][val_index]  # 以Key+val 作为字典的关键字保存值

    # 分割("enable=“,  )，处理完之后是这样的：[' enable=']
    key_value = {}
    for key_temp in val_dic:
        val_str = val_dic[key_temp]
        val_str_list = list(filter(not_empty, re.split("\(|\)|,", val_str)))
        #print(val_str_list)
        #print(key_temp)
        #print(val_str_list)
        #print(str_line)
        try:
            if len(val_str_list) == 1:
                # try:
                # print(key_temp)
                # print(val_str_list[0])
                # print(str_line.index(val_str_list[0]))
                key_value[key_temp] = str_line[
                                      int(str_line.index(val_str_list[0])) + int(len(val_str_list[0])):].strip()
                #print(key_value[key_temp])
            # except ValueError:
            #    continue
            elif len(val_str_list) == 2:
                # try:
                print("--*********")
                # print(key_temp)
                # print(val_str_list[0]+"-"+val_str_list[1])
                # print(str_line)
                #print(str_line.index(val_str_list[0]))
                #print(val_str_list[1])
                key_value[key_temp] = str_line[
                                      int(str_line.index(val_str_list[0])) + int(len(val_str_list[0])): int(
                                          str_line.index(val_str_list[1]))].strip()
                #print(key_value[key_temp])
            else:
                #print("val is none:" + str(len(val_str_list)))
                pass
        except ValueError:
            continue

        pass


def not_empty(s):
    return s and s.strip()


def fileread(dirlist, txtlist, file_config):  # 对比从config中读到的文件名和实际从log目录下搜到的文件之间的对比，只解析match上的文件
    samelist = match(dirlist, txtlist)
    log(Tag, samelist)
    log(Tag, dirlist)
    log(Tag, txtlist)
    log(Tag, file_config)
    if not check_excel_file(file_config):
        log(Tag, "config file is not exists")
        return
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_dict = get_sheet_name_key(file_config)
    # print("hurui1")
    # print(sheet_name_dict)
    merge_file_list.append(file_out_temp)
    for listtemp in samelist:
        # readfile = os.path.basename(listtemp)
        readfile = os.path.join(__file_in_base, os.path.basename(listtemp))
        log(Tag, "readfile:" + os.path.basename(readfile))
        log(Tag, "samelist:" + listtemp)
        __file__out = create(__file_out_base, intercept_file_name(listtemp))
        merge_file_list.append(__file__out)
        file_to_out = open(__file__out, "a+", encoding="UTF-8")
        log(Tag, "---------------")
        # readlogdebug(readfile, __file__out, file_config)
        thread_num = 1
        # 起始时间
        # start_time = time.clock()
        p = Partition(readfile, thread_num)
        t = []
        pos = p.part()
        # 生成线程
        for i in range(thread_num):
            t.append(Reader(readfile, file_to_out, sheet_name,sheet_name_dict, *pos[i],i))
            #t.append(Reader(readfile, file_to_out, file_config, fd.tell()))
        # 开启线程
        log_debug("thread_num")
        for i in range(thread_num):
            log_debug(t[i].thread_num)

        log(Tag, "start thread")
        for i in range(thread_num):
            t[i].start()

        for i in range(thread_num):
            t[i].join()
            log_debug("thread_numjoin")
            log_debug(t[i])
        # 等待所有线程完成
        log_debug("thread_num 2")
        file_to_out.close()

    """
    对多线程生成的文件做一个排序，为后续合并文件做准备
    """
    for sfile in merge_file_list:
        if sfile == file_out_temp:
            continue
        if checkFileSize(sfile) is False:
            merge_file_list.remove(sfile)
            continue
        SortedFile(sfile, sfile)
        pass
    """
    合并临时文件为最终文件
    """
    if len(merge_file_list) >= 2:
        while (1):
            if len(merge_file_list) < 2:
                break
                pass
            elif len(merge_file_list) == 2:
                merge_log(merge_file_list[0], merge_file_list[1], file_out_final, False)
                merge_file_list.remove(merge_file_list[1])
                pass
            else:
                merge_log(merge_file_list[0], merge_file_list[1], file_out_final, True)
                merge_file_list.remove(merge_file_list[1])
                pass
            pass
        pass
    pass


def read(mthreadID, dirlist):
    log(Tag, "---------------")
    log(Tag, dirlist)
    log(Tag, mthreadID)
    print("nihao ")
    pass


def readlogdebug(file__read, file_out, file_config):
    # 遍历所有的log文件，和所有的config，把符合keyword的行全部过滤出来
    log(Tag, "***---------")
    # log(Tag, file__read)
    # log(Tag, mthreadID)
    # print(file__read)
    trunk_size = 2 * 1024 * 1024
    if not check_excel_file(file_config):
        log(Tag, "config file is not exists")
        return
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_dict = get_sheet_name_key(file_config)
    print(sheet_name)
    # file_to_read = open(file__read, "r", encoding="UTF-8")
    file_to_out = open(file_out, "a", encoding="UTF-8")
    try:
        with open(file__read, 'r', encoding="UTF-8") as file_to_read:
            # while True:
            log(Tag, "strat read line")
            for lines in file_to_read.readlines(trunk_size):
                lines = lines.strip()
                if not lines:
                    log(Tag, "finish")
                    # yield lines
                    break
                # yield lines
                log(Tag, "start to read sheetname")
                for sheet_name_temp in sheet_name:
                    if "Logic Unit" in sheet_name_temp:  # 逻辑单元不参与
                        continue
                    if "Sheet" in sheet_name_temp:  # 逻辑单元不参与
                        continue
                    log(Tag, "sheet_name_temp-------------")
                    log(Tag, sheet_name_temp)
                    # threadLock.acquire()
                    config = sheet_name_dict[sheet_name_temp][0]
                    keyword_index = sheet_name_dict[sheet_name_temp][1]
                    level_index = sheet_name_dict[sheet_name_temp][2]
                    # threadLock.release()
                    # print(keyword_index)
                    # log(Tag, "read key")
                    for key in config:
                        if keyword_index > len(config[key]):
                            print("err")
                            continue
                        keyword = config[key][keyword_index]
                        level = config[key][level_index]
                        lines_level = lines.split()
                        log(Tag,len(lines_level))
                        if len(lines_level) < 5:
                            continue
                        log(Tag, "keyword---------1------")
                        log(Tag, level + lines_level[4])
                        if level not in lines_level[4]:
                            continue
                        # if "setWifiEnabled" in keyword:
                        #   break
                        log(Tag, "keyword-------2--------")
                        log(Tag, keyword)
                        if keyword in lines:
                            log(Tag, "file_out:" + file_out)
                            if "result" in file_out:  # 输出只是临时性文件，所以只负责存储有关键字信息
                                # threadLock.acquire()
                                write_file(lines, file_to_out, file_to_read)
                                # threadLock.release()
                                # decode_Logic_config(lines, config, key, tag_temp, sheet_name_temp)
                            else:
                                # 开始根据关键字来检查和提取关键性信息，并输出到output文件中#
                                # decode_Logic_config(lines, config, key, tag_temp, sheet_name_temp)
                                pass
                            pass
                        else:
                            continue
    finally:
        log(Tag, "file_to_out close")
        file_to_out.close()
        # config.clear()
        keyword_index = 0
        file_to_read.close()
    pass
    ###if (check_file_exist(file_out)):
    # merge_file_list.append(file_out)
    # a = changes_file_name(file_out, "test1.txt")
    # print(a)###


def get_sheet_name_key(file_config):
    # sheet list=[config(dict),keyword_index,level_index]
    # sheet_name_dict={sheetnameA-->listA;sheetnameB--> listB........}
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_list = []
    sheet_name_dict = {}
    print(sheet_name)
    for sheet_name_temp in sheet_name:
        sheet_name_list.clear()
        print(sheet_name_temp)
        if "Logic Unit" in sheet_name_temp:  # 逻辑单元不参与
            continue
        if "Sheet" in sheet_name_temp:  # 逻辑单元不参与
            continue
        log(Tag, "get_sheet_name_key")
        log(Tag, sheet_name_temp)
        config = get_all_config(file_config, sheet_name_temp)
        #print(config)
        tag_temp = get_tag(file_config, sheet_name_temp)
        keyword_index = find_tag(tag_temp[sheet_name_temp], "KEYWORD")
        level_index = find_tag(tag_temp[sheet_name_temp], "LEVEL")
        sheet_name_list.append(config)
        sheet_name_list.append(keyword_index)
        sheet_name_list.append(level_index)
        sheet_name_dict[sheet_name_temp] = deepcopy(sheet_name_list)
    return sheet_name_dict


class Reader(threading.Thread):
    def __init__(self, file__read, file_out, sheet_name, sheet_name_dict, start_pos, end_pos, thread_num):
        super(Reader, self).__init__()
        self.file_name = file__read
        self.fileout = file_out
        self.sheet_name = sheet_name
        self.sheet_name_dict = sheet_name_dict
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.thread_num = thread_num

    def run(self):
        # sheet_name = get_all_sheet_name(self.fileconfig)
        # sheet_name_dict = get_sheet_name_key(self.fileconfig)
        # file_to_read = open(file__read, "r", encoding="UTF-8")
        # file_to_out = open(self.fileout, "a", encoding="UTF-8")
        with open(self.file_name, 'rb') as file_to_read:
            '''
                    该if块主要判断分块后的文件块的首位置是不是行首，
                    是行首的话，不做处理
                    否则，将文件块的首位置定位到下一行的行首
            '''
            # print("self.start_pos")
            # print(self.start_pos)
            if self.start_pos != 0:
                file_to_read.seek(int(self.start_pos) - 1)
                if file_to_read.read(1) != '\n':
                    lines = file_to_read.readline()
                    self.start_pos = file_to_read.tell()
            file_to_read.seek(int(self.start_pos))
            '''
            对该文件块进行处理
            '''
            # while True:
            log_debug("strat read line--------------")
            log_debug(self.start_pos)
            log_debug(self.end_pos)
            log(Tag, "end line--------------")
            # self.end_pos = 49430528
            while (1):
                if self.start_pos >= self.end_pos:
                    break
                # print('行数',line_num)
                lines = file_to_read.readline()
                line = lines.decode('utf-8').strip()
                # log_debug(line)
                # if "WifiService" in line:
                # log_debug(line)
                if not len(line) or line.startswith('#'):
                    continue
                if not line:
                    log(Tag, "finish")
                    break
                # yield lines
                log(Tag, "start to read sheetname")
                jump_flag = False
                for sheet_name_temp in self.sheet_name:
                    if (jump_flag):
                        break
                    if "Logic Unit" in sheet_name_temp:  # 逻辑单元不参与
                        continue
                    if "Sheet" in sheet_name_temp:  # 逻辑单元不参与
                        continue
                    log(Tag, "sheet_name_temp-------------")
                    log(Tag, sheet_name_temp)
                    # print(sheet_name_temp)
                    # threadLock.acquire()
                    config = self.sheet_name_dict[sheet_name_temp][0]
                    # print(config)
                    keyword_index = self.sheet_name_dict[sheet_name_temp][1]
                    # print(keyword_index)
                    level_index = self.sheet_name_dict[sheet_name_temp][2]
                    # print(level_index)
                    # threadLock.release()
                    # print(keyword_index)
                    # log(Tag, "read key")
                    for key in config:
                        if keyword_index > len(config[key]):
                            print("err")
                            continue
                        keyword = config[key][keyword_index]
                        level = config[key][level_index]
                        lines_level = line.split()
                        log(Tag, len(lines_level))
                        if len(lines_level) < 5:
                            continue
                        log(Tag, "keyword---------1------")
                        log(Tag, level + lines_level[4])
                        # log_debug(line)
                        if level not in lines_level[4]:
                            # log_debug("continue")
                            continue
                        # log_debug(line)
                        if keyword in line:
                            # log_debug("self.fileout:")
                            # if "result" in self.fileout:  # 输出只是临时性文件，所以只负责存储有关键字信息
                            mutex.acquire()
                            write_file(line, self.fileout, file_to_read)
                            jump_flag = True
                            mutex.release()
                            break
                            # decode_Logic_config(line, config, key, tag_temp, sheet_name_temp)
                        # else:
                        # 开始根据关键字来检查和提取关键性信息，并输出到output文件中#
                        # decode_Logic_config(line, config, key, tag_temp, sheet_name_temp)
                        # pass
                    else:
                        pass
                self.start_pos = file_to_read.tell()
                if self.start_pos >= self.end_pos:
                    log_debug(self.start_pos)
            log_debug("while break self")
            log_debug(self.thread_num)


'''
对文件进行分块，文件块的数量和线程数量一致
'''
class Partition(object):
    def __init__(self, file_name, thread_num):
        self.file_name = file_name
        self.block_num = thread_num

    def part(self):
        fd = open(self.file_name, 'r')
        fd.seek(0, 2)
        pos_list = []
        file_size = fd.tell()
        log_debug("file_size:")
        log_debug(file_size)
        block_size = file_size / self.block_num
        start_pos = 0
        for i in range(self.block_num):
            if i == self.block_num - 1:
                end_pos = file_size - 1
                pos_list.append((start_pos, end_pos))
                break
            end_pos = start_pos + block_size - 1
            if end_pos >= file_size:
                end_pos = file_size - 1
            if start_pos >= file_size:
                break
            pos_list.append((start_pos, end_pos))
            start_pos = end_pos + 1
        fd.close()
        return pos_list


__file_in_base = os.path.join(os.getcwd(), "log")
__file_out_base = os.path.join(os.getcwd(), "result")
# __file__read = os.path.join(__file_in_base,"main.txt")

__file_in_base_1 = os.path.join(os.getcwd(), "config")
__file__config = os.path.join(__file_in_base_1, "Config.xlsx")
file_out_temp = os.path.join(__file_out_base, "test_temp.txt")
file_out_final = os.path.join(__file_out_base, "final_file.txt")

# filename = __file__read
# filename_output = __file__out
# read_excel(__file__config)

if __name__ == "__main__":
    list_all_files()
    dirlist = ["aplogcat-events.txt", "aplogcat-kernel.txt", "aplogcat-radio.txt", "aplogcat-main.txt",
               "aplogcat-system.txt"]
    mutex = threading.Lock()
    fileread(dirlist, file_txt_name(), __file__config)
