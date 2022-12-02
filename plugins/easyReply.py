# -*- coding: utf-8 -*-
import random
import sys

import json


#可以优化，bot.py中增加方式已经更新，但我懒得改
import openpyxl


def addReplys(ass):
    message=ass[2:]
    messageS=message.split('#')
    #读取字典
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    #print(dict)
    #print('---------')
    file.close()

    #对传入的字符串进行处理并加入字典
    #如果已经有关键字
    if (messageS[0] in dict):
        replyValue=dict.get(messageS[0])
        replyValue.append(messageS[1])
        print('已有关键字，追加')
        #print(replyValue)
    #没有关键字则创建
    else:
        dict[messageS[0]] = [messageS[1],]
        #print(dict)
    #重新写入

    #print(dict)
    js = json.dumps(dict)
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
    #print(type(dict))
    return dict
def add(key,value):
    file = open('Config\\dict.txt', 'r')
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
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
    #print(type(dict))
    return dict






def dels(messagess):
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    messageS=messagess[2:]
    try:
        dict.pop(messageS)
    except:
        print('没有指定的关键词')
        return 1
    js = json.dumps(dict)
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
    return dict

def delValue(key,valueNo):
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    if key in dict.keys():
        values=dict.get(key)
        try:
            value1=values.remove(valueNo)
            dict[key]=value1
        except:
            print('没有指定词')
    else:
        print('没有指定词')
    js = json.dumps(dict)
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
    return dict


def fromOut():
    file = open('Config\\dict.txt', 'r',encoding='utf-8')
    js = file.read()
    dicta = json.loads(js)
    print('已读取字典')
    # print(dict)
    # print('---------')
    file.close()

    xlsxPath = 'D:\Mirai\YirisVoiceGUI\PythonPlugins\Config\可爱系二次元bot词库1.5万词V1.1.xlsx'
    # 第一步打开工作簿
    wb = openpyxl.load_workbook(xlsxPath)
    # 第二步选取表单
    sheet = wb.active
    # 按行获取数据转换成列表
    rows_data = list(sheet.rows)
    # 获取表单的表头信息(第一行)，也就是列表的第一个元素
    titles = [title.value for title in rows_data.pop(0)]
    print(titles)

    all_row_dict = []
    newDict = {}
    # 遍历出除了第一行的其他行
    for a_row in rows_data:
        the_row_data = [cell.value for cell in a_row]
        # 将表头和该条数据内容，打包成一个字典
        row_dict = dict(zip(titles, the_row_data))
        # print(row_dict)
        all_row_dict.append(row_dict)
    for i in all_row_dict:
        key = i.get('问题')
        value = i.get('回复(把{name}替换为ai对聊天对象的称呼，根据{segment}切分为多次发送的句子)')
        # print('key:'+key+' '+'value:'+value)
        dicta[key] = value
    print(dicta)
    js = json.dumps(dicta)
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
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
    fromOut()
