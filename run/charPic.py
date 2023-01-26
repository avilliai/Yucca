# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from plugins.charPicture import painter


def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| charPic module loaded successfully 已加载--- 字符画 ---模块')
    global sendera
    sendera = 0
    global zifuhua
    zifuhua = 0
    @bot.on(GroupMessage)
    async def charPic(event: GroupMessage):
        if str(event.message_chain).startswith('字符画'):
            if event.message_chain.count(Image)==1:
                lst_img = event.message_chain.get(Image)
                print('已接收命令')
                await bot.send(event,'正在生成.....请稍候....')
                path=painter(lst_img[0].url)
                await bot.send(event,Image(path=path))
                # print(lst_img[0].url)
            else:
                await bot.send(event,'请发送一张图片哦')
                global zifuhua
                global sendera
                sendera=event.sender.id
                zifuhua=1


    @bot.on(GroupMessage)
    async def charPic1(event: GroupMessage):
        global zifuhua
        global sendera
        if zifuhua==1 :
            if event.sender.id==sendera:
                if event.message_chain.count(Image)==1:
                    lst_img = event.message_chain.get(Image)
                    print('已接收命令')
                    await bot.send(event,'正在生成.....请稍候....')
                    path=painter(lst_img[0].url)
                    await bot.send(event,Image(path=path))
                    zifuhua=0
                    # print(lst_img[0].url)
                else:
                    await bot.send(event,'请发送一张图片哦')
                    zifuhua=1