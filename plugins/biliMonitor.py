#!/usr/bin/python
# _*_ coding:utf-8 _*_
import asyncio
from mirai.models.message import At
import requests
import json
from mirai.exceptions import ApiError
from mirai import Startup, GroupMessage
from mirai.models import AtAll
from asyncio import sleep
import os

sleepTime = 5
s = ''
groupINFO = []


# [[[389391931],[69731917,'null',"0","0","null"]],#[[[群号，群号,......],[b站号,'',"0","0",""]],[[群号，群号,......],[b站号,'',"0","0",""]],......]
# [[517814646],[1553878284,'null',"0","0","null"]]]
def popTail(s):
    ls = list(s)
    ls.pop(ls.__len__() - 1)
    return ''.join(ls)


with open(os.path.dirname(__file__) + '\\Config\\bili-live.txt', 'r', encoding='utf-8') as file:
    temp = file.read()
    ls = temp.split("*")
    ls.pop(ls.__len__() - 1)
    ls2 = []
    flage = True
    temp = []
    temp2 = []
    for i in ls:
        if flage == True:
            temp = i.split(" ")
            # print(temp)
            flage = False
        else:
            temp2 = i.split(" ")
            # print(temp2)
            flage = True
            groupINFO.append([temp, temp2])
    file.close()


def getLive(i):
    global groupINFO
    url = "https://api.bilibili.com/x/space/acc/info?mid=" + str(groupINFO[i][1][0])
    pythondy = json.loads(requests.get(url).text)  # json对象转换为python字典
    groupINFO[i][1][1] = pythondy['data']['name']
    groupINFO[i][1][2] = str(pythondy['data']['live_room']['liveStatus'])
    groupINFO[i][1][4] = str(pythondy['data']['live_room']['url'])


def writeTxt():
    s = ""
    for i in groupINFO:
        for j in i:
            for k in j:
                s += str(k) + " "
            s = popTail(s)
            s += "*"
    with open(os.path.dirname(__file__) + '\\config\\bili-live.txt', 'w', encoding='utf-8') as file:
        file.write(s)
        file.close()


def main(bot):
    async def Print(bot):
        global groupINFO
        for i in range(0, groupINFO.__len__()):
            if groupINFO[i][1][2] != groupINFO[i][1][3]:
                groupINFO[i][1][3] = groupINFO[i][1][2]
                for group in groupINFO[i][0]:
                    if groupINFO[i][1][2] == "1":
                        await bot.send_group_message(group, groupINFO[i][1][1] + "检测到直播开始\n地址：" + groupINFO[i][1][4])
                    elif groupINFO[i][1][2] == "0":
                        await bot.send_group_message(group, groupINFO[i][1][1] + "直播结束了")

    @bot.on(Startup)
    async def bili_live(event: Startup):
        print("bilibili-live加载成功")
        while True:
            for i in range(0, groupINFO.__len__()):
                getLive(i)
                await Print(bot)
            print("循环成功")
            await sleep(30)

    @bot.on(GroupMessage)
    async def addUser(event: GroupMessage):
        global groupINFO
        if "添加 live/" in event.message_chain:
            temp = str(event.message_chain)
            temp2 = temp.split("/")
            s = temp2[1]
            for i in range(0, groupINFO.__len__()):
                if s == groupINFO[i][1][0]:
                    for j in groupINFO[i][0]:
                        if str(event.group.id) == j:
                            return bot.send(event, "已经添加过了呢")
                    groupINFO[i][0].append(str(event.group.id))
                    writeTxt()
                    print(groupINFO)
                    return bot.send(event, "添加成功")
            groupINFO.append([[str(event.group.id)], [s, 'null', '0', '0', 'null']])
            print(groupINFO)
            writeTxt()
            return bot.send(event, "添加成功")
