import os
import time


def source_exist(dirpath):
    return os.path.exists(dirpath) and os.path.isdir(dirpath)


def get_entries(dirpath, condition=None, sleep=3):
    while True:
        if not os.path.exists(dirpath):
            print("Provided dirpath {} doesn't exist.".format(dirpath))
            print('Waiting {} seconds...'.format(sleep))
            time.sleep(sleep)
        else:
            break

    while True:
        if not os.path.isdir(dirpath):
            print("Provided dirpath {} is not directory.".format(dirpath))
            print('Waiting {} seconds...'.format(sleep))
            time.sleep(sleep)
        else:
            break

    if not condition:
        condition = lambda a: True

    while True:
        entries = os.listdir(dirpath)
        entries = sorted([f for f in entries if condition(dirpath, f)])
        entries_len = len(entries)
        print('Found {} entries.'.format(entries_len))
        if entries_len == 0:
            print('Waiting {} seconds...'.format(sleep))
            time.sleep(sleep)
        else:
            break

    return entries


# helper condition functions for get_entries


def check_file(dirpath, item):
    return not item.startswith('.') and os.path.isfile(os.path.join(dirpath, item))


def check_dir(dirpath, item):
    return not item.startswith('.') and os.path.isdir(os.path.join(dirpath, item))


