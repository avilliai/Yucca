# -*- coding: UTF-8 -*-
import random
import sys

import json


# 可以优化，bot.py中增加方式已经更新，但我懒得改
import time


def adduser(ass):

    file = open('Config\\userInfo.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    # print(dict)
    # print('---------')
    file.close()

    # 对传入的字符串进行处理并加入字典
    # 如果已经有关键字
    if (ass in dict):
        return
        print('已有关键字，追加')
        # print(replyValue)
    # 没有关键字则创建
    else:
        times=time.localtime()
        dict[ass] = times
        print(time.mktime(times))
    # 重新写入
    # print(dict)
    js = json.dumps(dict)
    file = open('Config\\userInfo.txt', 'w')
    file.write(js)
    file.close()
    # print(type(dict))
    return '注册成功啦\n'+str(time.strftime('%Y-%m-%d %H:%M:%S', times))







def query(messagess):
    file = open('Config\\userInfo.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    dict.get(messagess)


    return dict




#with open("config\\replyDic.txt",'a') as f:
if __name__ == '__main__':

    while True:
        s=input('输入命令')

        print(adduser(s))


