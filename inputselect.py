import os
import tkinter.filedialog

def selectbyUser():
    while(1):
        list = []
        select = int(input())
        print(select)
        if select == "\n" :
            break
        elif select == "\r" :
            list.append(select)
    return list


def showlist(mlist):
    # 文件对话框：
    for mlist_temp in mlist:
       print(mlist_temp)

"""
mlist = ["a","b","c","d","e","f"]
showlist(mlist)
print(selectbyUser())
"""

