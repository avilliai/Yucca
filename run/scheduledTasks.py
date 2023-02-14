# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys
from asyncio import sleep

from fuzzywuzzy import fuzz,process
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai import Startup, Shutdown
from mirai.models import BotJoinGroupEvent, MemberCardChangeEvent
from mirai.models.events import NudgeEvent
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from MoeGoe import voiceGenerate
from plugins.RandomStr.RandomStr import random_str
from plugins.gitZen import get_zen
from plugins.moyu import moyu
from plugins.newsEveryday import news
from readConfig import readConfig
from trans import translate


def main(bot):
    time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time1 + '| scheduler module loaded successfully 已加载--- 定时任务 ---模块')

    file = open('Config/moyu/groups.txt', 'r')
    js = file.read()
    global severGroups
    global severGroupsa
    severGroupsa = json.loads(js)
    severGroups = severGroupsa.keys()

    time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time1 + '| 定时任务服务群聊读取完毕')


    # 这里是定时任务区
    # 定时摸鱼,可以在Config//moyu//中添加群
    global scheduler
    scheduler = AsyncIOScheduler()

    @bot.on(Startup)
    def start_scheduler(_):
        scheduler.start()  # 启动定时器
        print('当前路径' + sys.argv[0])
        Path = sys.argv[0][:-20]

    @bot.on(Shutdown)
    def stop_scheduler(_):
        scheduler.shutdown(True)  # 结束定时器

    # 摸鱼人日历
    @scheduler.scheduled_job(CronTrigger(hour=16, minute=55))
    async def timer():
        moyuPic = moyu()
        for i in severGroups:
            intTrans = int(i)
            await sleep(5)
            try:
                await bot.send_group_message(intTrans, Image(path=moyuPic))
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群' + str(intTrans) + '不存在或已退出')

    @scheduler.scheduled_job(CronTrigger(hour=13, minute=49))
    async def timer():
        for i in severGroups:
            intTrans = int(i)
            await sleep(4)
            try:
                out = 'plugins/voices/sing/24.mp3'
                await bot.send_group_message(intTrans, Voice(path=out))

                await bot.send_group_message(intTrans, '正在播放:' + 'my heart is yours and yours alone-Moon Jelly')
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群' + str(intTrans) + '不存在或已退出')


    @scheduler.scheduled_job(CronTrigger(hour=17, minute=50))
    async def timer():
        global severGroups
        for i in severGroups:
            intTrans = int(i)
            index = random.randint(1, 5)
            await sleep(3)
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 下班时间-----> ')
            if index == 1:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('啊......好累呢，该下班了') + '[JA]'
            if index == 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]到下班时间了......晚上去哪里玩呢?...[JA]'
            if index == 3:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('辛苦了，要注意休息哦。') + '[JA]'
            if index > 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('今天也好好努力过了......今天也很棒了') + '[JA]'
            voiceGenerate(tex, out)
            try:
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群'+str(intTrans)+'不存在或已退出')

    # 早八新闻自动推送
    @scheduler.scheduled_job(CronTrigger(hour=7, minute=40))
    async def timer():
        newsPic = news()
        global severGroups
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time + '| 新闻事件-----> ')
        for i in severGroups:
            intTrans = int(i)
            ranpath = random_str()
            out ='plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('早上好........已经为您整理好了今天的新闻！.......有什么有趣的事情吗?') + '[JA]'
            voiceGenerate(tex, out)
            try:
                await bot.send_group_message(intTrans, Image(path=newsPic))
                await sleep(2)
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群' + str(intTrans) + '不存在或已退出')

    # 中午推送github禅语
    @scheduler.scheduled_job(CronTrigger(hour=12, minute=10))
    async def timer():
        global severGroups
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time1 + '| 禅语-----> ')
        for i in severGroups:
            intTrans = int(i)
            ranpath = random_str()
            out ='plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('中午好，这是今天的禅语......') + '[JA]'
            voiceGenerate(tex, out)
            zen = await get_zen()
            try:
                await bot.send_group_message(intTrans, zen)
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群' + str(intTrans) + '不存在或已退出')

    # 早八问候
    @scheduler.scheduled_job(CronTrigger(hour=8, minute=1))
    async def timer():
        global severGroups
        for i in severGroups:
            intTrans = int(i)
            index = random.randint(1, 4)
            time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time1 + '| 执行早八问候-----> ')
            if index == 1:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('早上好......记得吃早饭~......今天也请好好加油~！') + '[JA]'
            if index == 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('唔......早上好呀!') + '[JA]'
            if index == 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('起床啦~!.......现在还没起床的话可不行') + '[JA]'
            voiceGenerate(tex, out)
            try:
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time1 + '| 指定群' + str(intTrans) + '不存在或已退出')
    # 追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event: GroupMessage):
        if str(event.message_chain).startswith('添加群#'):
            global severGroupsa
            global severGroups
            s = str(event.message_chain).split('#')
            severGroupsa[str(s[1])]=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            severGroups=severGroupsa.keys()
            newData = json.dumps(severGroupsa)
            with open('Config/moyu/groups.txt', 'w') as fp:
                fp.write(newData)

    @bot.on(GroupMessage)
    async def autoAdd(event: GroupMessage):
        global severGroupsa
        global severGroups
        if str(event.group.id) not in severGroupsa.keys():
            severGroupsa[str(event.group.id)]=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            severGroups=severGroupsa.keys()
            newData = json.dumps(severGroupsa)
            time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time1 + '| 新增群：'+str(event.group.id))
            with open('Config/moyu/groups.txt', 'w') as fp:
                fp.write(newData)