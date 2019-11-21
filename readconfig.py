import os
import re
from copy import deepcopy
from datetime import datetime

import xlrd

#sheet_list = ["WiFi on-off_P","WiFi connect-disconnect_P"]  # 定义哪些模块config需要被扫描


sheet_version = ["Parse-P"]
sheet_white_list = []
#debug_DBG =False
debug_DBG =True


# test API
def read_excel(ExcelFile):
    pass


def log_debug(logstr):
    if debug_DBG:
        print(str(str(datetime.now()) + ":   " + str(logstr)))
    pass


def get_all_sheet_name(ExcelFile):  # 获取excel所有的工作表，返回类型为list
    worktable = xlrd.open_workbook(ExcelFile)
    all_work_sheet = worktable.sheet_names()
    # print(all_work_sheet)
    return all_work_sheet
    pass


def get_all_config(ExcelFile, sheet_name):  # 根据提供的sheetname来把所有的行转换为以tag为唯一key的字典，返回类型为字典
    if "Logic" in sheet_name:  # 逻辑单元不参与
        return -1

    worktable = xlrd.open_workbook(ExcelFile)
    sheet = worktable.sheet_by_name(sheet_name)
    sheet_name_dict = {}
    i = 1
    while i < sheet.nrows:
        rows = sheet.row_values(i)
        sheet_name_dict[rows[0]] = rows
        i = i + 1
    return sheet_name_dict
    pass


def get_tag(ExcelFile, sheet_name):  # 根据excel中sheetname返回tag，类型为字典
    """
    :type sheet_name: str
    """
    worktable = xlrd.open_workbook(ExcelFile)
    sheet = worktable.sheet_by_name(sheet_name)
    tag = {}
    rows = sheet.row_values(0)
    tag[sheet_name] = rows
    # print(tag)
    return tag


def find_tag(tag_list, str):  # 根据每个字典的tag中的list和str来返回list中的具体的位置
    # print(tag_list.index(str))
    try:
        return tag_list.index(str)
    except ValueError:
        return -1


def excel_cols(ExcelFile, sheet_name):
    worktable = xlrd.open_workbook(ExcelFile)
    sheet = worktable.sheet_by_name(sheet_name)
    # print(sheet.name, sheet.nrows, sheet.ncols)
    return sheet.ncols


def get_str_from_dict(dict, tag, index):  # <key,list>的字典中的list中获取对应位置的str
    return dict[tag][index]
    pass


def get_sheet_name_key(file_config, msheet_list, mdecode):
    # sheet list=[config(dict),keyword_index,level_index]
    # sheet_name_dict={sheetnameA-->listA;sheetnameB--> listB........}
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_list = []
    sheet_name_dict = {}
    print(sheet_name)
    flag = False
    for sheet_name_temp in sheet_name:
        sheet_name_list.clear()
        if len(msheet_list) < 1:
            msheet_list = ["WiFi on-off_P", "WiFi connect-disconnect_P"]
        log_debug("Parse sheet name: " + str(msheet_list))
        log_debug("real sheet name: " + str(sheet_name_temp))
        for mlist in msheet_list:
            log_debug("mlist: " + str(mlist))
            if mlist == sheet_name_temp:
                flag = True
                print(sheet_name_temp + " is match")
                break
            else:
                continue

        if flag is False:
            print(sheet_name_temp + " is not match")
            continue

        if "Logic Unit" in sheet_name_temp:  # 逻辑单元不参与
            continue
        if "Sheet" in sheet_name_temp:  # 逻辑单元不参与
            continue
        config = get_all_config(file_config, sheet_name_temp)
        # print(config)
        tag_temp = get_tag(file_config, sheet_name_temp)
        keyword_index = 0
        level_index = 0
        if mdecode is False:
            keyword_index = find_tag(tag_temp[sheet_name_temp], "KEYWORD")
            level_index = find_tag(tag_temp[sheet_name_temp], "LEVEL")
            sheet_name_list.append(config)
            sheet_name_list.append(keyword_index)
            sheet_name_list.append(level_index)
            if keyword_index < 0 or level_index < 0:
                print("keyword_index and level index is wrong")
            sheet_name_dict[sheet_name_temp] = deepcopy(sheet_name_list)
        else:
            sheet_name_list.append(config)
            sheet_name_list.append(tag_temp)
            sheet_name_dict[sheet_name_temp] = deepcopy(sheet_name_list)
        log_debug("sheet_name_dict : " + str(sheet_name_dict))
        return sheet_name_dict


def get_sheet_version(file_config):
    # sheet list=[config(dict),keyword_index,level_index]
    # sheet_name_dict={sheetnameA-->listA;sheetnameB--> listB........}
    sheet_name = get_all_sheet_name(file_config)
    sheet_name_list = []
    sheet_name_dict = {}
    # print(sheet_name)
    flag = False
    for sheet_name_temp in sheet_name:
        sheet_name_list.clear()
        for mlist in sheet_version:
            if mlist in sheet_name_temp:
                flag = True
                break
            else:
                continue

        if flag is False:
            continue
        # print(sheet_name_temp)
        flag = False
        config = get_all_config(file_config, sheet_name_temp)
        # print(config)
        tag_temp = get_tag(file_config, sheet_name_temp)
        # Item_index = find_tag(tag_temp[sheet_name_temp], "Item")
        Function_index = find_tag(tag_temp[sheet_name_temp], "Function")
        for key in config:
            # sheet_name_list.append(config[key][Item_index])
            sheet_name_list.append(config[key][Function_index])
        sheet_name_dict[sheet_name_temp] = deepcopy(sheet_name_list)
    log_debug("get_sheet_version: " + str(sheet_name_dict))
    return sheet_name_dict  # {'Parse-P': ['WiFi on-off_P', 'WiFi connect-disconnect_P', 'WiFi scan', 'Hotspot', 'P2P', 'Default (all)']}


def filter_valid_sheet(file_config, mdecode):
    version_dict = get_sheet_version(file_config)
    sheet_list = []
    log_debug("version_dict:" + str(version_dict))
    for sheet_temp in version_dict.keys():
        for mlist in version_dict[sheet_temp]:
            sheet_list.append(mlist)
    return get_sheet_name_key(file_config, sheet_list, mdecode)
    pass


def get_sheet_list_value(sheet_name,
                         tag_temp):  # 返回类型为dict，{sheetname:{{keyward:keyward_index},{level:level_index},{MANDATORY:MANDATORY_index},......}}
    value_dict = {}
    temp_dict = {}
    # config[key][keyword_index]
    for temp in tag_temp[sheet_name]:
        if temp == "logs" or temp == "Note":
            continue
        temp_dict[temp] = find_tag(tag_temp[sheet_name], temp)
    value_dict[sheet_name] = deepcopy(temp_dict)
    return value_dict


# __file_in_base = os.path.join(os.getcwd(), "config")
# ExcelFile = os.path.join(__file_in_base, "Config.xlsx")
__file_in_base_1 = os.path.join(os.getcwd(), "config")
__file__config = os.path.join(__file_in_base_1, "Config.xlsx")


# print(get_sheet_version(__file__config))
# print(get_sheet_name_key(__file__config))
# filter_valid_sheet(__file__config)
# read_excel(ExcelFile)


def decode_val(line, str):  # str 暂时只能用逗号分开，加其他的符号容易引起误会
    if str.isspace():
        print("continue")
        return None
    if ",#" not in str:
        print("please use ',#' to split string in excel(value col)")
        return None
    config_value = str.split(",#")
    print(len(config_value[0]))
    print(len(config_value[1]))
    if len(config_value[0]) <= 0 and len(config_value[1]) <= 0:
        return None
        pass
    elif len(config_value[0]) > 0 and len(config_value[1]) <= 0:
        start_index = re.search(config_value[0].strip(), line).span()
        print(start_index)
        return line[start_index[1] + 1:].strip()
        pass
    elif len(config_value[0]) > 0 and len(config_value[1]) > 0:
        start_index = re.search(config_value[0].strip(), line).span()
        end_index = re.search(config_value[1].strip(), line).span()
        if start_index > end_index:
            return line[start_index[1] + 1:end_index[0]].strip()
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


"""
ex:
{11000.0: '', 11099.0: 'Turn on WiFi failed', 11100.0: '', 11199.0: 'Turn off WiFi failed'}
dict[key:output2] ---> key: int; output2:str
"""


def get_complete_process_dict(sheet_name_dict):
    complete_process_dict = {}
    for sheet_name_temp in sheet_name_dict:
        if "Logic Unit" in sheet_name_temp:  # 逻辑单元不参与
            continue
        if "Sheet" in sheet_name_temp:  # 逻辑单元不参与
            continue
        config = sheet_name_dict[sheet_name_temp][0]  # 取TAG 值
        tag_temp = sheet_name_dict[sheet_name_temp][1]
        index = get_sheet_list_value(sheet_name_temp, tag_temp)
        process_index = index[sheet_name_temp]["PROCESS"]
        output2_index = index[sheet_name_temp]["OUTPUT2"]
        for key in config:
            process_value = config[key][process_index]
            output2_value = config[key][output2_index]
            complete_process_dict[process_value] = output2_value
            pass
    return complete_process_dict

    # list_temp = re.split(r'\breason=\b.\blocally_generated\b',line)
    # print(list_temp)
    # last = list[1].split("locally_generated")
    # print(last[0].strip())
    # start_index = line.find(list[0])+ len(list[0])+1
    # end_index = list[1]
    # print(list[0])
    # print(start_index)

# line = "aaa reason=3 locally_generated=1 disconnect_rssi=14 -->2019-11-05-17-58aplogcat-main -->test_temp"
# print(decode_val(line,""))
