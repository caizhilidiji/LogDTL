import os
import difflib
import time
from getTrainAndTestLogs import *

file = r'/myData\originData'


def getLogs(file, path, save):
    type = ''
    with open('result/2k_log_raw', 'a') as r:
        with open(path, 'r') as f:
            lines = f.readlines()
            logs = []

            if file in ['alert']:
                type = 'ips'
                logs = getSnortLog(lines)

            if '_top.log' in file:
                type = 'sys'
                logs = getSysLog(lines)

            if file in ['iptables.log']:
                type = 'firewall'
                logs = getLineLog(lines)

            data = {
                'Content': [],
                'Event': [],
                'EventTemplate': [],
                'EventStr': []
            }

            for l in logs:
                template = getLogTemplate(l, type)
                # print(l)
                if save:
                    r.write(l)
                data['Content'].append(l)
                data['Event'].append(template[0])
                data['EventTemplate'].append(template[1])
                data['EventStr'].append(template[2])

            if save or True:
                df = pandas.DataFrame(data)
                df.to_csv('result/log_train_test.csv', index=False, mode='a')


# 处理源日志为单行
def getLineLog(lines):
    return lines


# 处理源日志为ips
def getSnortLog(lines):
    logs = []
    current_log = ""
    for line in lines:
        if line.strip() == "":
            logs.append(current_log.strip().replace('\n', ' '))
            current_log = ""
        else:
            current_log += line
    return logs


# 下为判断字符串是否为%Y-%m-%d格式，其他格式同理。
def is_valid_date(strdate):
    '''
    判断是否是一个有效的日期字符串
    2023-06-09 23:19:27.586523
    '''
    try:
        time.strptime(strdate, "%Y-%m-%d %H:%M:%S.%f")
        return True
    except:
        return False


# 处理系统日志
def getSysLog(lines):
    logs = []
    current_log = ""
    for line in lines:
        # print(line)
        if line.strip() == "":
            logs.append(current_log.strip().replace('\n', ' '))
            current_log = ""
            continue
        if is_valid_date(line.replace('\n', '')):
            # print(line)
            current_log = line
            continue

        current_log += line

    return logs


if __name__ == '__main__':
    # print(templatesDic)
    # getSnortLog(f'D:\Study_笔记\研究生毕业设计\code\LogDTL\myData\originData\\net_1686320048.032491\\alert')
    # https://blog.csdn.net/sazass/article/details/98071353
    for root, dirs, files in os.walk(file):
        for file in files:
            path = os.path.join(root, file)
            # print(file)
            # print(path)
            getLogs(file, path, save=False)
