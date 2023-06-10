import time


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

if __name__ == '__main__':
    print(is_valid_date('2023-06-09 23:19:27.586523'))