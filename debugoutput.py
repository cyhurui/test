from datetime import datetime

debug_v =True
debug_i =True
debug_d =True
debug_e =True


def logi(tag, logstr):
    if (debug_i):
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
        print()
    pass

def log_d(tag,logstr):
    if debug_d:
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
        print()
    pass

def log_e(tag,logstr):
    if debug_e:
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
        print()
    pass


def log_v(tag,logstr):
    if debug_v:
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
        print()
    pass