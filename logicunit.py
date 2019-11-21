#!/usr/bin/python

import os, time, sys, re
from copy import deepcopy

from debugoutput import log_v, log_e
from mergefile import outputdate

output1 = ""
output2 = ""

# logic_dict: {process:logic_list},ex:{110:[00,01,02,03,04,.....]}
logic_dict = {}
# logic_list: [00,01.02.03,04......],process number
logic_list = []
tag = "logicunit"


def logicdispatch_debug(logic_dict, line):
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
    # parse the logic unit, e.g: 'L1 (VAL1,true)', 'L2(KEYWORD)'
    lu = logic_dict['LOGIC UNIT']  # like 'L1 (VAL1,true)'
    # print(lu)
    # get the logic: L1, L2...
    # print(logic)
    logic_all = decode_val_logic(lu)  # ["L1","Val1",true]
    process_val = logic_dict["PROCESS"]
    if unit_check(logic_all):
        add_process_dict(process_val)
        pass
    else:
        log_e(tag, "")
        pass
    pass


def add_process_dict(process_val):
    global logic_dict
    logic_list = []
    key_list = get_process_dict_key(process_val)
    log_v(tag, "add_process_dict:")
    log_v(tag, key_list)
    if key_list[1] == 99:  # Need to clear dict
        if reset_dict(key_list[0]):
            log_e(tag, "process code is 99, it mean the process finish and will start new process")
        return
        pass
    if key_list[0] not in logic_dict:
        logic_list.append(key_list[1])
        logic_dict[key_list[0]] = deepcopy(logic_list)
    else:
        # print(str(logic_dict[key_list[1]]))
        logic_list = deepcopy(logic_dict[key_list[0]])
        logic_list.append(key_list[1])
        logic_dict[key_list[0]] = deepcopy(logic_list)
    pass

def get_process_dict():
    return logic_dict
    pass


def get_process_dict_key(process_val):
    key_list = []
    key_list.append(int(int(process_val) / 100))
    key_list.append(int(int(process_val) % 100))
    return key_list





def unit_check(logic_all):
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

    # parse the logic unit, e.g: 'L1 (VAL1,true)', 'L2(KEYWORD)'
    lu = logic_dict['LOGIC UNIT']  # like 'L1 (VAL1,true)'
    # print(lu)

    # get the logic: L1, L2...
    logic = lu[:2]
    # print(logic)

    # module, submodule, process, subprocess
    # For example: 11201
    # module: wifi(1) (1: wifi; 2: BT; 3: LBS; 4: NFC)
    # submodule: sta(1) (1: station; 2: softap; 3: p2p)
    # process: connect(2) (0: wifi on; 1: wifi off; 2: wifi connect; 3: wifi disconnect; 4: wifi scan)
    # subprocess: (01), (00 ~ 99, 99 means the subprocess is end, other values mean it is working)

    # switch logic unit
    # todo: parameters valid check
    if logic == "L1":
        # logic1(VAL1, true/false)
        val1 = logic_dict['VAL1']
        para = lu.split(",", 1)  # para now is 'true)' or 'false)'
        para1 = para.rstrip("）")  # delete the ')' on the right
        # print("val1", val1, "para1: ", para1)
        return logic1(val1, para1)
    elif logic == "L2":
        print("start L2")
        keyword = logic_dict['KEYWORD']
        print("keyword: ", keyword)
        return logic2(keyword)
    elif logic == "L3":
        # print("start L3")
        keyword = logic_dict['KEYWORD']
        return logic3(keyword, line)
    elif logic == "L4":
        print("start L4")
        keyword = logic_dict['KEYWORD']
        # todo: how to define para1?
        return logic4(keyword, "debug")
    else:
        # print("logic unit is wrong: ", L)
        # return fail
        pass
    # todo: clear the args list?
    pass


def logic1(val, para):
    # print("running L1")
    if val == para:
        print(output1)  # output to the file
        return True
    else:
        print(output2)  # output to the file
        return False
    pass


def logic2(keyword):
    # print("running L2")
    if keyword:
        print(output1)  # output to the files
    else:
        print(output2)  # output to the file
    return True
    # pass


def logic3(keyword, line):
    # print("running L3")
    if keyword:
        line_date = outputdate(line)
        print(output1)  # error log, output to the files
        print(line_date)  # and print the line
        # print (line)
        # todo: stop the current logic flow
        return False  # need stop the current logic flow
    else:
        print(output2)
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
            i = 0
            return
        # else:
        #   continue
        # todo: check whether this logic is reasnonalbe
    else:
        print(output2)

    pass


def reset_dict(key):
    global logic_dict
    print(logic_dict)
    logic_dict[key].clear()
    print("after reset: ", logic_dict)
    return True


def delete_dict(key):
    global logic_dict
    print("key: ", key)
    del logic_dict[key]
    print("after delete: ", logic_dict)
    return True


str = ["11000", "11010", "11020", "11030", "11040", ]
for i in str:
    print(add_process_dict(i))
print(get_process_dict())