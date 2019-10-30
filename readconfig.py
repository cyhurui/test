import os
import xlrd


# test API
def read_excel(ExcelFile):
    pass


def get_all_sheet_name(ExcelFile):  # 获取excel所有的工作表，返回类型为list
    worktable = xlrd.open_workbook(ExcelFile)
    all_work_sheet = worktable.sheet_names()
    #print(all_work_sheet)
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

# __file_in_base = os.path.join(os.getcwd(), "config")
# ExcelFile = os.path.join(__file_in_base, "Config.xlsx")
# read_excel(ExcelFile)
