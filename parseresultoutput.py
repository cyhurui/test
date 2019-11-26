import os, time, sys

parse_result_file = ""


# create new file based on current time
def get_parse_result_file():
    current_path = sys.path[0]
    print("current_path: ", current_path)
    folder_existed = 0

    for root, dirs, files in os.walk(current_path):
        print("dirs: ", dirs)
        if 'result' in dirs:
            folder_existed = 1
            print("dirs have included 'result' folder")
            break

    if folder_existed == 0:
        os.mkdir(current_path, 'result')
        print("create 'result' sub folder")

    file_dir = os.path.join(current_path, 'result')
    print("file_dir: ", file_dir)

    # create file name
    file_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    complete_file_name = file_time + '_parse_result' + '.txt'
    path = os.path.join(file_dir, complete_file_name)
    return path


def open_parse_result_file():
    file = get_parse_result_file()
    global parse_result_file
    parse_result_file = open(file, 'x', encoding='utf-8')
    pass


# output the parse result to file
def write_to_parse_result_file(str):
    return parse_result_file.write(str+"\n")


# close file
def close_parse_result_file():
    parse_result_file.close()
    pass
