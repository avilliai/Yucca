# -*- coding: utf-8 -*-
import json

import openpyxl
from openpyxl import load_workbook


def importDict():
    #xlsxPath = 'D:\Mirai\YirisVoiceGUI\PythonPlugins\Config\可爱系二次元bot词库1.5万词V1.1.xlsx'
    xlsxPath = 'D:\Mirai\YirisVoiceGUI\PythonPlugins\Config\词库.xlsx'
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
    newDict={}
    # 遍历出除了第一行的其他行
    for a_row in rows_data:
        the_row_data = [cell.value for cell in a_row]
        # 将表头和该条数据内容，打包成一个字典
        row_dict = dict(zip(titles, the_row_data))
        #print(row_dict)
        all_row_dict.append(row_dict)
    for i in all_row_dict:
        key=i.get('问题')
        #value=i.get('回复(把{name}替换为ai对聊天对象的称呼，根据{segment}切分为多次发送的句子)')
        value = i.get('回复(把yucca替换成ai对自己的称呼，例如ai的名字(推荐)、我、咱等等，把name替换为ai对聊天对象的称呼，根据,切分为多次发送的句子)')

        if (key in newDict):
            replyValue=newDict.get(key)
            replyValue.append(value)
            print('已有关键字，追加')
            #print(replyValue)
        #没有关键字则创建
        else:
            newDict[key] = [value,]
        #print('key:'+key+' '+'value:'+value)
    print(newDict)
    js = json.dumps(newDict)
    file = open('Config\superDict.txt', 'w')
    file.write(js)
    file.close()
def formExist():
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    outdictkeys=dict.keys()

    file = open('Config\\superDict.txt', 'r')
    jss = file.read()
    newDict = json.loads(jss)
    mohuKeys = newDict.keys()
    print('已读取模糊匹配字典')

    '''for sss in outdictkeys:
        key = sss
        value=dict.get(sss)

        if (key in mohuKeys):
            replyValue = newDict.get(key)
            for sasa in value:
                replyValue.append(sasa)
                print('已有关键字，追加')
            # print(replyValue)
        # 没有关键字则创建
        else:
            newDict[key] = value
        # print('key:'+key+' '+'value:'+value)'''

def Merge(dict1, dict2):
    return (dict2.update(dict1))


    # 返回  None
    print(Merge(dict1, dict2))

    # dict2 合并了 dict1
    print(dict2)



    '''js = json.dumps(newDict)
    file = open('Config\\superDict.txt', 'w')
    file.write(js)
    file.close()
    print(newDict)'''



if __name__ == '__main__':
    importDict()
