# 此模块提供日志相关操作
import time
import os


def get_log_path(file_path, name_path):
    file_name = str.split(name_path, '.')
    me_name = file_name[-1]
    tmp_path = me_name.replace('.', '\\')
    pos = file_path.find(tmp_path)
    project_path = file_path[:pos]
    name_list = str.split(me_name, '.')
    file_name = name_list.pop()
    file_time = time.strftime("%Y%m%d%H%M%S")
    log_name = f'{file_name}_{file_time}.txt'
    tmp = 'logs\\'
    for name in name_list:
        tmp = f'{tmp}{name}\\'
    log_dir = project_path + tmp
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = log_dir + log_name

    return log_path


def log(file_path, msg, mode='a+', encoding='utf-8'):
    print(msg)
    fp = open(file=file_path, mode=mode, encoding=encoding)
    fp.write(msg)
    fp.write('\n')
    fp.close()

# print(get_log_path(r'E:\中森\dingdangcode_autotest\ui_auto\testcase\test_field\add_draft.py', 'add_draft'))
# print(get_log_path(r'E:\中森\dingdangcode_autotest\ui_auto\testcase\main_process\edu_main_process.py',
# 'ui_auto.testcase.main_process.edu_main_process'))
