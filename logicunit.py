#!/usr/bin/python

import os, time, sys, re
from copy import deepcopy

from debugoutput import log_v, log_e
from mergefile import outputdate
from parseresultoutput import open_parse_result_file, write_to_parse_result_file, close_parse_result_file

output1 = ""
output2 = ""

# process_sub_dict: {process:logic_list},ex:{110:[00,01,02,03,04,.....]}
process_sub_dict = {}
# logic_list: [00,01.02.03,04......],process number
logic_list = []
tag = "logicunit"

# complete_dict format:
# {'110': {'01': 'output1', '02': 'output2', '03': 'output3', '04': 'output4', ... '99': 'output99'},
#  '111': {'01': 'output11', '02': 'output21', '03': 'output31', '04': 'output41', ..., '99': 'output99'}}
complete_dict = {}


def logicdispatch(logic_dict, line):
    """
        logic_dict: format:
        {'TAG': 'wifi_on_2', 'LEVEL': 'D', 'KEYWORD': 'client mode active', 'MANDATORY': 11099, 'VALUE_FLAG': 0.0,
        'VAL1': '', 'VAL2': '', 'VAL3': '', 'LOGIC UNIT': 'L2 (KEYWORD)', 'OUTPUT1': 'Turned on WiFi', 'OUTPUT2': 'Turn on WiFi failed'}
        """
    # obtain the output string firstly
    global output1
    output1 = logic_dict['OUTPUT1']
    global output2
    output2 = logic_dict['OUTPUT2']

    # open the parse result file to output
    open_parse_result_file()

    # parse the logic unit, e.g: 'L1 (VAL1,true)', 'L2(KEYWORD)'
    lu = logic_dict['LOGIC UNIT']  # like 'L1 (VAL1,true)'

    logic_all = decode_val_logic(lu)  # ["L1","Val1",true]
    process_val = logic_dict["PROCESS"]
    if unit_check(logic_all, logic_dict):
        add_process_dict(process_val)
        pass
    else:
        log_e(tag, "")
        pass
    pass


def add_process_dict(process_val):
    global process_sub_dict
    logic_list = []
    key_list = get_process_dict_key(process_val)
    log_v(tag, "add_process_dict:")
    log_v(tag, key_list)
    if key_list[1] == 99:  # Need to clear dict
        if reset_dict(key_list[0]):
            log_e(tag, "process code is 99, it mean the process finish and will start new process")
        return
        pass
    if key_list[0] not in process_sub_dict:
        logic_list.append(key_list[1])
        process_sub_dict[key_list[0]] = deepcopy(logic_list)
    else:
        # print(str(process_sub_dict[key_list[1]]))
        logic_list = deepcopy(process_sub_dict[key_list[0]])
        logic_list.append(key_list[1])
        process_sub_dict[key_list[0]] = deepcopy(logic_list)
    pass

def get_process_dict():
    return process_sub_dict
    pass


def get_process_dict_key(process_val):
    key_list = []
    key_list.append(int(int(process_val) / 100))
    key_list.append(int(int(process_val) % 100))
    return key_list


def unit_check(logic_all,logic_dict):
    # module, submodule, process, subprocess
    # For example: 11201
    # module: wifi(1) (1: wifi; 2: BT; 3: LBS; 4: NFC)
    # submodule: sta(1) (1: station; 2: softap; 3: p2p)
    # process: connect(2) (0: wifi on; 1: wifi off; 2: wifi connect; 3: wifi disconnect; 4: wifi scan)
    # subprocess: (01), (00 ~ 99, 99 means the subprocess is end, other values mean it is working)

    # switch logic unit
    # todo: parameters valid check
    logic_unit = logic_all[0]
    if logic_unit == "L1":
        # logic1(VAL1, true/false)
        val = logic_dict[logic_all[1]]
        # print("val1", val1, "para1: ", para1)
        return logic1(val, logic_all[2])
    elif logic_unit == "L2":
        print("start L2")
        keyword = logic_dict['KEYWORD']
        print("keyword: ", keyword)
        return logic2(keyword)
    elif logic_unit == "L3":
        # print("start L3")
        keyword = logic_dict['KEYWORD']
        return logic3(keyword, "debug")
    elif logic_unit == "L4":
        print("start L4")
        keyword = logic_dict['KEYWORD']
        # todo: how to define para1?
        return logic4(keyword, "debug")
    else:
        # print("logic unit is wrong: ", L)
        return -1
    # todo: clear the args list?
    pass


def decode_val_logic(lu):  # ['L1(VAL1', 'true)'] or
    list = []
    logic = lu.replace("\n", "").replace("\r", "").replace(" ", "").strip().split(",")
    if len(logic) == 2:  # ['L1(VAL1', 'true)']
        list.append(logic[0][:2])
        list.append(logic[0][3:7])
        list.append(logic[1])
    elif len(logic) == 1:
        list.append(logic[0][:2])
        pass
    else:
        log_e("please re-defined logic:")
        log_e(tag, logic)
    return list

def logic1(val, para):
    if val == para:
        print(output1)
        write_to_parse_result_file(output1)
        return True
    else:
        print(output2)
        write_to_parse_result_file(output2)
        return False
    pass


def logic2(keyword):
    # print("running L2")
    if keyword:
        print(output1)
        write_to_parse_result_file(output1)
    else:
        print(output2)
        write_to_parse_result_file(output2)
    return True
    # pass


def logic3(keyword, line):
    # print("running L3")
    if keyword:
        line_date = outputdate(line)
        print(output1)  # error log, output to the files
        write_to_parse_result_file(output1)
        print(line_date)  # and print the line
        # print (line)
        write_to_parse_result_file(line)
        # todo: stop the current logic flow
        return False  # need stop the current logic flow
    else:
        print(output2)
        write_to_parse_result_file(output2)
        return True
    pass


# Some key logs print many times, just output once
# e.g.: "FORGET_NETWORK" is printed for three times, just print one time
# 151171 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  ConnectedState !FORGET_NETWORK uid=1000 rt=131457/131457 0 0
# 151172 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  L2ConnectedState !FORGET_NETWORK uid=1000 rt=131457/131457 0 0
# 151173 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  ConnectModeState !FORGET_NETWORK uid=1000 rt=131458/131458 0 0
def logic4(keyword, n):
    # print("running L4")
    i = 0
    if keyword:
        i = i + 1
        if i >= n:
            print(output1)
            write_to_parse_result_file(output1)
            i = 0
            return
        # else:
        #   continue
        # todo: check whether this logic is reasnonalbe
    else:
        print(output2)
        write_to_parse_result_file(output2)
    pass


def reset_dict(key):
    global process_sub_dict
    print(process_sub_dict)
    process_sub_dict[key].clear()
    print("after reset: ", process_sub_dict)
    return True


def delete_dict(key):
    global process_sub_dict
    print("key: ", key)
    del process_sub_dict[key]
    print("after delete: ", process_sub_dict)
    return True

#str = ["11000", "11010", "11020", "11030", "11040", ]
#for i in str:
#    print(add_process_dict(i))
#print(get_process_dict())

def set_complete_process_dict(process_dict):
    global complete_dict
    complete_dict = deepcopy(process_dict)
    pass

def get_complete_process_dict():
    return complete_dict
    pass


# all logs are handled done, clear the process_dict
def clear_process_dict():
    global process_sub_dict

    for key in process_sub_dict:
        val_list = process_sub_dict[key]
        print("val_list: ", val_list)

        the_last_process = val_list[-1]
        print("The last process is: ", the_last_process)
        print("The key is: ", key)

        if the_last_process == 99:
            print("The process is completed, skip")
            continue
        else:
            # complete_dict format:
            # {'110': {'01': 'output1', '02': 'output2', '03': 'output3', '04': 'output4', ... '99': 'output99'},
            #  '111': {'01': 'output11', '02': 'output21', '03': 'output31', '04': 'output41', ..., '99': 'output99'}}
            complete_dict = get_complete_process_dict()

            # e.g: key = '110', subprocess = {'01': 'output1', '02': 'output2', '03': 'output3', '04': 'output4'
            # subprocess = {'01': 'output1', '02': 'output2', '03': 'output3', '04': 'output4'}
            subprocess = complete_dict[key]
            print("The subprocess is: ", subprocess)

            # find the next key of 'the_last_process'
            if len(subprocess) and the_last_process in subprocess:
                # change the subprocess to list
                key_list = list(subprocess.keys())
                print("key_list: ", key_list)
                # the index of 'the_last_process'
                index = key_list.index(the_last_process)
                print("The last process index: ", index)

                # the next key of of 'the_last_process'
                next_key = key_list[index + 1]
                if next_key in subprocess:
                    next_output2 = subprocess[next_key]
                    print("next_output2: ", next_output2)  # write to the files
                    write_to_parse_result_file(next_output2)
            else:
                print("Cannot find the last process in complete_dict")

    process_sub_dict.clear()
    close_parse_result_file()

    print("after clear_process_dict: ", process_sub_dict)
    pass