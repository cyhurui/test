import os
import re
import threading

from logicunit import logicdispatch, clear_process_dict, get_complete_dict, set_complete_dict
from mergefile import intercept_file_name, merge_log, SortedFile, checkFileSize
from readdir import check_excel_file, create, check_file_exist
from readdir import match
from readconfig import get_all_sheet_name, filter_valid_sheet, get_sheet_list_value, get_complete_process_dict

from datetime import datetime

dict = {}
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


def decode_Logic_config(fliepath, sheet_name_dict):
    if check_file_exist(fliepath) is not True:
        file_out = open(fliepath, 'w')
        file_out.close()
        log_debug("final_file.txt is non-exit")
        return
        pass
    with open(fliepath, 'rb') as file_to_read:
        # while True:
        while (1):
            lines = file_to_read.readline()
            line = lines.decode('utf-8').strip()
            #print(line)
            if not line:
                clear_process_dict()
                log(Tag, "finish")
                break
            if not len(line) or line.startswith('#'):
                continue
            jump_flag = False
            # flag = False
            for sheet_name_temp in sheet_name_dict:
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
                config = sheet_name_dict[sheet_name_temp][0]  # 取TAG 值
                # print(config)
                tag_temp = sheet_name_dict[sheet_name_temp][1]  # KEYWORD 值
                # print(tag_temp)
                # level_index = sheet_name_dict[sheet_name_temp][2]  # 取LEVEL
                index = get_sheet_list_value(sheet_name_temp, tag_temp)

                # print(index)
                keyword_index = index[sheet_name_temp]["KEYWORD"]
                level_index = index[sheet_name_temp]["LEVEL"]
                if keyword_index < 0:
                    continue
                for key in config:
                    if keyword_index > len(config[key]):
                        print("err")
                        continue
                    keyword = config[key][keyword_index]
                    level = config[key][level_index]
                    lines_level = line.split()
                    if len(lines_level) < 5:  # 保证格式是时间+进程号+log等级，格式不同的，直接不处理
                        continue
                    if len(level) >= 1:  # config中是有log的 level等级的
                        if level not in lines_level[4]:  # 这个逻辑需要添加log的等级，可以加快扫描速度
                            # print("continue")
                            continue
                    # log_debug(line))
                    if keyword in line:
                        log_debug("self.fileout:")
                        logic_value = []
                        """
                        logic_dict: format:
                        {'TAG': 'wifi_on_2', 'LEVEL': 'D', 'KEYWORD': 'client mode active', 'MANDATORY': 1.0, 'VALUE_FLAG': 0.0, 
                        'VAL1': '', 'VAL2': '', 'VAL3': '', 'LOGIC UNIT': 'L2 (KEYWORD)', 'OUTPUT1': 'Turned on WiFi', 'OUTPUT2': 'Turn on WiFi failed'}
                        """
                        logic_dict = {}
                        for value_temp in index[sheet_name_temp]:
                            # print(value_temp)
                            if "VALUE_FLAG" in value_temp:
                                logic_dict[value_temp] = config[key][index[sheet_name_temp][value_temp]]
                                continue
                            elif "VAL" in value_temp:
                                logic_dict[value_temp]=decode_val(line,config[key][index[sheet_name_temp][value_temp]])
                            else:
                                logic_dict[value_temp] = config[key][index[sheet_name_temp][value_temp]]
                        # write_file(line, fileout, file_to_read)
                        logicdispatch(logic_dict, line)
                        jump_flag = True
                        break
                        # decode_Logic_config(line, config, key, tag_temp, sheet_name_temp)
                    else:
                        continue
                    # 开始根据关键字来检查和提取关键性信息，并输出到output文件中#
                    # decode_Logic_config(line, config, key, tag_temp, sheet_name_temp)
                    # pass
    pass


def decode_val(line, value):  # str 暂时只能用逗号分开，加其他的符号容易引起误会
    if value.isspace():
        print("continue")
        return None
    if ",#" not in value:
        if len(value) > 1:
            print("please use ',#' to split string in excel(value col)")
        return None
    config_value = value.split(",#")
    end_index = re.search("-->", line).span()
    if len(config_value[0]) <= 0 and len(config_value[1]) <= 0:
        return None
        pass
    elif len(config_value[0]) > 0 and len(config_value[1]) <= 0:
        start_index = re.search(config_value[0].strip(), line).span()
        print(start_index)
        return line[start_index[1]:end_index[0]].strip()
        pass
    elif len(config_value[0]) > 0 and len(config_value[1]) > 0:
        start_index = re.search(config_value[0].strip(), line).span()
        end_index = re.search(config_value[1].strip(), line).span()
        if start_index > end_index:
            return line[start_index[1]:end_index[0]].strip()
        else:
            print("")
        pass
    elif len(config_value[0]) <= 0 and len(config_value[1]) > 0:
        end_index = re.search(config_value[1].strip(), line).span()
        return line[0:end_index[0]].strip()
    else:
        print("this config is error, please check excel")
        return None
        pass

def not_empty(s):
    return s and s.strip()

# 对比从config中读到的文件名和实际从log目录下搜到的文件之间的对比，只解析match上的文件
def fileread(dirlist, txtlist, file_config):
    samelist = match(dirlist, txtlist)
    log(Tag, samelist)
    log(Tag, dirlist)
    log(Tag, txtlist)
    log(Tag, file_config)
    if not check_excel_file(file_config):
        log(Tag, "config file is not exists")
        return
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_dict = filter_valid_sheet(file_config, False)
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
            t.append(Reader(readfile, file_to_out, sheet_name, sheet_name_dict, *pos[i], i))
            # t.append(Reader(readfile, file_to_out, file_config, fd.tell()))
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
    print(merge_file_list)
    sheet_name_dict = filter_valid_sheet(file_config, True)  # dict{list{dict{list},}}
    set_complete_dict(get_complete_process_dict(sheet_name_dict))
    #decode_Logic_config(merge_file_list[0], sheet_name_dict)
    decode_Logic_config(file_out_final, sheet_name_dict)



def read(mthreadID, dirlist):
    log(Tag, "---------------")
    log(Tag, dirlist)
    log(Tag, mthreadID)
    print("nihao ")
    pass


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
                flag = False
                for sheet_name_temp in self.sheet_name_dict:
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
                    config = self.sheet_name_dict[sheet_name_temp][0]  # 取TAG 值
                    # print(config)
                    keyword_index = self.sheet_name_dict[sheet_name_temp][1]  # KEYWORD 值
                    # print(keyword_index)
                    level_index = self.sheet_name_dict[sheet_name_temp][2]  # 取LEVEL
                    if keyword_index < 0:
                        continue
                    for key in config:
                        if keyword_index > len(config[key]):
                            print("err")
                            continue
                        keyword = config[key][keyword_index]
                        level = config[key][level_index]
                        lines_level = line.split()
                        log(Tag, len(lines_level))
                        # print("----------------")
                        # print(level)
                        # print(lines_level[4])
                        if len(lines_level) < 5:  # 保证格式是时间+进程号+log等级，格式不同的，直接不处理
                            continue
                        log(Tag, "keyword---------1------")
                        log(Tag, level + lines_level[4])
                        # log_debug(line)

                        if len(level) >= 1:  # config中是有log的 level等级的
                            if level not in lines_level[4]:  # 这个逻辑需要添加log的等级，可以加快扫描速度
                                # print("continue")
                                continue
                        # log_debug(line))
                        if keyword in line:
                            log_debug("self.fileout:")
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
mutex = threading.Lock()
# filename = __file__read
# filename_output = __file__out
# read_excel(__file__config)
sheet_name_dict = filter_valid_sheet(__file__config, True)  # dict{list{dict{list},}}
#set_complete_process_dict(get_complete_process_dict(sheet_name_dict))
#print(get_process_dict())

#print(dict)
#decode_Logic_config(file_out_final,sheet_name_dict)
"""
dict = {}
dict1={1:"1",2:"2"}
dict[0] = dict1
dict[0][3] = 5
#decode_Logic_config(file_out_final,sheet_name_dict)
# temp_dict = {"10010": 12, "10002": 32, "10000": 45}
# temp_dict = sorted(temp_dict.items(), key=lambda d: d[0])
# print(temp_dict)
str = "uid=1000 enable=true -->2019-11-25-18-11aplogcat-main"
val = "enable=,#"
print(decode_val(str,val))
"""
