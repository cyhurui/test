from datetime import datetime

debug_v = False
debug_i = True
debug_d = True
debug_e = True


def logi(tag, logstr):
    if (debug_i):
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
    pass


def log_d(tag, logstr):
    if debug_d:
        print()
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
    pass


def log_e(tag, logstr):
    if debug_e:
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
    pass


def log_v(tag, logstr):
    if debug_v:
        print(str(datetime.now()) + "  " + str(tag) + ":   " + str(logstr))
    pass
