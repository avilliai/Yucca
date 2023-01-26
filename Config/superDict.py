# -*- coding: utf-8 -*-
import json

import openpyxl
from openpyxl import load_workbook

#此方法用于更新词库
def importDict(mode):
    #xlsxPath = 'D:\Mirai\YirisVoiceGUI\PythonPlugins\Config\可爱系二次元bot词库1.5万词V1.1.xlsx'
    if mode==1:
        xlsxPath = 'Config\词库.xlsx'
    else:
        xlsxPath = 'Config\完全匹配.xlsx'
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

    #当你需要向已有词库导入时取消注释
    '''fileaa = open('Config\\superDict.txt', 'r')
    js1 = fileaa.read()
    newDict = json.loads(js1)
    print('已读取现存字典')'''

    #新建词库，当你需要新建词库时取消注释
    newDict={}

    # 遍历出除了第一行的其他行
    for a_row in rows_data:
        the_row_data = [cell.value for cell in a_row]
        # 将表头和该条数据内容，打包成一个字典
        row_dict = dict(zip(titles, the_row_data))
        #print(row_dict)
        all_row_dict.append(row_dict)
    for i in all_row_dict:
        if mode==1:
            key=i.get('问题')#表格第一列列名
            #第二列列名
            value = i.get('回复(把{me}替换成ai对自己的称呼，例如ai的名字(推荐)、我、咱等等，把{name}替换为ai对聊天对象的称呼，根据{segment}切分为多次发送的句子)')
        else:
            key=i.get('key')
            value=i.get('value')

        if (key in newDict):
            replyValue=newDict.get(key)
            if value in replyValue:
                print('已存在该回复，不添加')
            else:
                replyValue.append(value)
                print('已有关键字，追加')
            #print(replyValue)
        # 没有关键字则创建
        else:
            newDict[key] = [value,]
        #print('key:'+key+' '+'value:'+value)
    print(newDict)
    js = json.dumps(newDict)
    if mode==1:
        file = open('Config\superDict.txt', 'w')
    else:
        file = open('Config\Dict.txt', 'w')
    file.write(js)
    file.close()





if __name__ == '__main__':
    importDict(1)
    importDict(2)
