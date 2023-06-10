import os
import difflib
import time

file = r'D:\Study_笔记\研究生毕业设计\code\LogDTL\dataPreprocess\originData'


# print(difflib.SequenceMatcher(None, Str, s3).quick_ratio())

def getLogs(file, path):
    if file in ['alert']:
        getSnortLog(path)

    if '_top.log' in file:
        getSysLog(path)

    if file in ['iptables.log']:
        getLineLog(path)


# 处理源日志为单行
def getLineLog(path):
    with open('data/logs.txt', 'a') as r:
        with open(path, 'r') as f:
            for line in f.readlines():
                r.write(line)


# 处理源日志为snort
def getSnortLog(path):
    with open('data/logs.txt', 'a') as r:
        with open(path, 'r') as f:
            lines = f.readlines()
            logs = []
            current_log = ""
            for line in lines:
                if line.strip() == "":
                    logs.append(current_log.strip().replace('\n', ' '))
                    current_log = ""
                else:
                    current_log += line

            for l in logs:
                r.write(l + '\n')


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
def getSysLog(path):
    with open('data/logs.txt', 'a') as r:
        with open(path, 'r') as f:
            lines = f.readlines()
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

            for l in logs:
                r.write(l + '\n')

    pass


if __name__ == '__main__':
    # getSnortLog(f'D:\Study_笔记\研究生毕业设计\code\LogDTL\dataPreprocess\originData\\net_1686320048.032491\\alert')
    # https://blog.csdn.net/sazass/article/details/98071353
    for root, dirs, files in os.walk(file):
        for file in files:
            path = os.path.join(root, file)
            # print(file)
            # print(path)
            getLogs(file, path)
