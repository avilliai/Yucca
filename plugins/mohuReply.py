# -*- coding: utf-8 -*-
import random
import sys

import json


#可以优化，bot.py中增加方式已经更新，但我懒得改
import openpyxl
from fuzzywuzzy import fuzz


def mohuaddReplys(ass):
    message=ass[2:]
    messageS=message.split('#')
    #读取字典
    file = open('Config/superDict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    #print(dict)
    #print('---------')
    file.close()

    #对传入的字符串进行处理并加入字典
    #如果已经有关键字
    if (messageS[0] in dict):
        replyValue = dict.get(messageS[0])
        replyValue.append(messageS[1])
        print('已有关键字，追加')
        # print(replyValue)
    # 没有关键字则创建
    else:
        dict[messageS[0]] = [messageS[1], ]
        #print(dict)
    #重新写入

    #print(dict)
    js = json.dumps(dict)
    file = open('Config/superDict.txt', 'w')
    file.write(js)
    file.close()
    #print(type(dict))
    return dict
def mohuadd(key,value):
    file = open('Config/superDict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    #print(dict)
    #print('---------')
    file.close()

    dict[key] = value
        #print(dict)
    #重新写入
    #print(dict)
    js = json.dumps(dict)
    file = open('Config/superDict.txt', 'w')
    file.write(js)
    file.close()
    #print(type(dict))
    return dict






def mohudels(messagess):
    file = open('Config/superDict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    messageS=messagess[4:]
    try:
        dict.pop(messageS)
    except:
        print('没有指定的关键词')
        return 1

    js = json.dumps(dict)
    file = open('Config/superDict.txt', 'w')
    file.write(js)
    file.close()
    return dict

def mohudelValue(key,valueNo):
    file = open('Config/superDict.txt', 'r')
    js = file.read()
    dict = json.loads(js)

    if key in dict.keys():
        values = dict.get(key)
        try:
            value1 = values.remove(valueNo)
            dict[key] = value1
        except:
            print('error')
    else:
        print('没有指定词')
    js = json.dumps(dict)
    file = open('Config/superDict.txt', 'w')
    file.write(js)
    file.close()
    return dict



#with open("config\\replyDic.txt",'a') as f:
if __name__ == '__main__':
    '''print('当前路径' + sys.argv[0])
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    print(dict)
    while True:
        s=input('输入命令')
        if s.startswith('添加'):
            print(addReplys(s))
        elif s.startswith('删除'):
            print(dels(s))'''
    mohudels('模糊删除图片')

