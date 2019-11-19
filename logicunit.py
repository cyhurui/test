#!/usr/bin/python

import os, time, sys, re

# return status code
fail = -1
success = 0

output1 = ""
output2 = ""

"""
def getargs(arglist):
    global local_list
    local_list = arglist
    #print("local_list in getargs: ", local_list)
    global output1
    output1 = local_list[3]
    global output2
    output2 = local_list[4]
    pass
"""

 # arglist should be logicunit, keyword, para1, output1，output2，val1，val2...
def logicdispatch(logic_dict):

    """
    def logicdispatch(arglist):
    # get args. only gets the args that
    getargs(arglist)
    logicunit = local_list[0]
    #print("logicunit in logicdispatch: ", logicunit)
    keyword = local_list[1]
    #print("keyword in logicdispatch: ", keyword)
    para1 = local_list[2]

    # ignorecase if needed
    # lu = logicunit.upper()

    logic_dict: format:
    {'TAG': 'wifi_on_2', 'LEVEL': 'D', 'KEYWORD': 'client mode active', 'MANDATORY': 1.0, 'VALUE_FLAG': 0.0,
    'VAL1': '', 'VAL2': '', 'VAL3': '', 'LOGIC UNIT': 'L2 (KEYWORD)', 'OUTPUT1': 'Turned on WiFi', 'OUTPUT2': 'Turn on WiFi failed'}
    """
    logicunit = logic_dict['LOGIC UNIT']
    #print(logicunit)
    L = logicunit[:2]
    #print(L)

    global output1
    output1 = logic_dict['OUTPUT1']
    global output2
    output2 = logic_dict['OUTPUT2']

    # switch logic unit
    # todo: parameters valid check
    if L == "L1":
        val1 = logic_dict['VAL1']
        print("val1", val1)
        return logic1(val1)
    elif L == "L2":
        print("start L2")
        keyword = logic_dict['KEYWORD']
        print("keyword: ", keyword)
        return logic2(keyword)
    elif L == "L3":
        #print("start L3")
        keyword = logic_dict['KEYWORD']
        return logic3(keyword)
    elif L == "L4":
        print("start L4")
        keyword = logic_dict['KEYWORD']
        #todo: how to define para1?
        logic4(keyword, para1)
    else:
        print("logic unit is wrong: ", L)
        return fail
    # todo: clear the args list?
    pass

def logic1(val):
    #print("running L1")
    if val == "true":
        print(output1 + " is true")
        return success
    elif val == "false":
        print(output2)
        return success
    else:
        print("val is not expected: ", val1)
        return fail
    pass


def logic2(keyword):
    #print("running L2")
    if keyword:
        print(output1)
    else:
        print(output2)
    return 0
    #pass


def logic3(keyword):
    #print("running L3")
    if keyword:
        print(output1) #error log
        return -1  # need stop the logic flow
    else:
        print(output2)
        return 0
    pass


# Some key logs print many times, just output once
# e.g.: "FORGET_NETWORK" is printed for three times, just print one time
# 151171 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  ConnectedState !FORGET_NETWORK uid=1000 rt=131457/131457 0 0
# 151172 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  L2ConnectedState !FORGET_NETWORK uid=1000 rt=131457/131457 0 0
# 151173 07-04 15:30:43.574  1789  2271 D WifiStateMachine:  ConnectModeState !FORGET_NETWORK uid=1000 rt=131458/131458 0 0
def logic4(keyword, n):
    #print("running L4")
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
