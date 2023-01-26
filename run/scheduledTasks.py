# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys
from fuzzywuzzy import fuzz,process
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai import Startup, Shutdown
from mirai.models import BotJoinGroupEvent, MemberCardChangeEvent
from graiax import silkcoder
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
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| scheduler module loaded successfully 已加载--- 定时任务 ---模块')
    severGroups = readConfig(r"Config\moyu\groups.txt")
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| 已读取服务群聊')
    # 这里是定时任务区
    # 定时摸鱼,可以在Config//moyu//中添加群
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
    @scheduler.scheduled_job(CronTrigger(hour=16, minute=50))
    async def timer():
        moyuPic = moyu()
        for i in severGroups:
            intTrans = int(i)
            time.sleep(5)
            try:
                await bot.send_group_message(intTrans, Image(path=moyuPic))
            except:
                print('摸鱼日历发送出错')

    @scheduler.scheduled_job(CronTrigger(hour=16, minute=49))
    async def timer():
        global severGroups
        for i in severGroups:
            intTrans = int(i)
            index = random.randint(1, 5)
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 下班时间-----> ')
            if index == 1:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('啊......好累呢，该下班了') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]到下班时间了......晚上去哪里玩呢?...[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('辛苦了，要注意休息哦。') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index > 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('今天也好好努力过了......今天也很棒了') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))

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
                time.sleep(5)
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                print('没有对应的群')

    # 中午推送github禅语
    @scheduler.scheduled_job(CronTrigger(hour=12, minute=10))
    async def timer():
        global severGroups
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time + '| 禅语-----> ')
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
                print('没有对应的群')

    # 早八问候
    @scheduler.scheduled_job(CronTrigger(hour=8, minute=1))
    async def timer():
        global severGroups
        for i in severGroups:
            intTrans = int(i)
            index = random.randint(1, 4)
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 执行早八问候-----> ')
            if index == 1:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('早上好......记得吃早饭~......今天也请好好加油~！') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('唔......早上好呀!') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('起床啦~!.......现在还没起床的话可不行') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))