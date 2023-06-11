# 生成训练集和测试集所需的格式
import difflib
import re

from pandas import *


def getEventStr(input_str):
    output_str = re.sub(r'\b\w+\b', 'DES', input_str)
    # print(output_str)
    output_str = re.sub(r'<\*>', 'VAR', output_str)
    # print(output_str)
    return output_str


def getLogEvents(save):
    templatesDic = {}

    df = read_csv('result/chatgpt_log_events.csv')
    for row_idx, row in df.iterrows():
        # print(row['EventTemplate'])
        output_string = re.sub(r'<\w+>', '<*>', row['EventTemplate']).strip()
        # 多个连续空格合并成一个空格
        output_string = re.sub(r"\s+", " ", output_string)
        # print(output_string)
        row['EventTemplate'] = output_string
        eventStr = getEventStr(output_string)
        if row['Type'] not in templatesDic:
            templatesDic[row['Type']] = [[row['EventId'], output_string,eventStr]]
        else:
            templatesDic[row['Type']].append([row['EventId'], output_string.strip(),eventStr])

    if save:
        df.to_csv('result/2k_log_events.csv', index=False)

    return templatesDic


def getLogTemplate(log, type):
    # print("-------------------------------")
    score = 0
    Template = None
    for template in templatesDic[type]:
        # print(template[1])
        # print(log)
        ts = difflib.SequenceMatcher(None, log, template[1]).quick_ratio()
        if ts > score:
            Template = template
            score = ts

    return Template


templatesDic = getLogEvents(False)

if __name__ == '__main__':
    getLogEvents(False)
