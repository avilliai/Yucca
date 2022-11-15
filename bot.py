import json
import random
import os

import aiohttp
import mirai.models.events

import asyncio
import datetime

from mirai import Mirai, WebSocketAdapter, Startup, Shutdown, Face
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain 
from pygments import plugin

from MoeGoe import voiceGenerate

import sys

from plugins import biliMonitor
from plugins.Covid import getCovid

from plugins.RandomStr.RandomStr import random_str
from plugins.abstractMess import emoji,pinyin
from plugins.charPicture import painter
from plugins.cpGenerate import get_cp_mesg
from plugins.easyReply import addReplys, dels
from plugins.gitZen import get_zen
from plugins.jokeMaker import get_joke

from plugins.moyu import moyu
from plugins.newsEveryday import news
from plugins.peroDog import pero_dog_contents
from plugins.picGet import pic
from readConfig import readConfig
from trans import translate

if __name__ == '__main__':
    bot = Mirai(3093724179, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))
    #翻字典
    '''file = open('plugins\\Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print(dict)
    file.close()
    keyReply = dict.keys()'''
    #私聊内容
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain) == '你好':
            await bot.send(event, 'Hello World!')

    #监听群聊消息
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'test':
            await bot.send_group_message(699455559, 'yucca测试版YIRIS启动成功！')

            # print(str(event.message_chain))  # 打印消息内容

    @bot.on(mirai.models.events.NudgeEvent)
    async def handle_nudge_message(event: mirai.models.events.NudgeEvent):
       await bot.send_nudge(target=1840094972,subject=3093724179,kind='Friend')

    #图片模块
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        #if str(event.message_chain) == '/pic':
        if '/pic' in str(event.message_chain):
            picNum=int((str(event.message_chain))[4:])
            if picNum<10 and picNum>-1:
                for i in range(picNum):
                    a = pic()
                    await bot.send(event, Image(path=a))
            elif picNum=='':
                a = pic()
                await bot.send(event, Image(path=a))
            else:
                await bot.send(event,"可以发点正常的数字吗")


    # 摸鱼
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain)=='摸鱼':
             moyus=moyu()
             await bot.send(event, Image(path=moyus))

    #这里是定时任务区
    #定时摸鱼,可以在Config//moyu//中添加群
    scheduler = AsyncIOScheduler()
    @bot.on(Startup)
    def start_scheduler(_):
        scheduler.start()  # 启动定时器
        print('当前路径' + sys.argv[0])
        Path=sys.argv[0][:-20]
    @bot.on(Shutdown)
    def stop_scheduler(_):
        scheduler.shutdown(True)  # 结束定时器
    #摸鱼人日历
    @scheduler.scheduled_job(CronTrigger(hour=16, minute=50))
    async def timer():
        moyuPic=moyu()
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            await bot.send_group_message(intTrans, Image(path=moyuPic))

    @scheduler.scheduled_job(CronTrigger(hour=16, minute=49))
    async def timer():
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            index = random.randint(1, 4)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('啊......好累呢，该下班了') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[ZH]辛苦了，要注意休息哦~[ZH]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('辛苦了，要注意休息哦~') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))

    #早八新闻自动推送
    @scheduler.scheduled_job(CronTrigger(hour=7, minute=40))
    async def timer():
        newsPic = news()
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            await bot.send_group_message(intTrans, Image(path=newsPic))
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('早上好~........已经为您整理好了今天的新闻！.......有什么有趣的事情吗?') + '[JA]'
            voiceGenerate(tex, out)
            await bot.send_group_message(intTrans, Voice(path=out))

    #中午推送github禅语
    @scheduler.scheduled_job(CronTrigger(hour=12, minute=10))
    async def timer():
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('中午好，这是今天的禅语......') + '[JA]'
            voiceGenerate(tex, out)
            zen = await get_zen()
            await bot.send_group_message(intTrans, zen)
            await bot.send_group_message(intTrans, Voice(path=out))

    #早八问候
    @scheduler.scheduled_job(CronTrigger(hour=8, minute=1))
    async def timer():
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            index = random.randint(1, 4)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('早上好......记得吃早饭~......今天也请好好加油~！') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = 'D:\\Mirai\\Yiris\\PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('唔......早上好呀!') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = 'D:\\Mirai\\Yiris\\PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('起床啦~!.......现在还没起床的话可不行') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))

    #早八新闻
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '新闻':
            newPic = news()
            await bot.send(event, Image(path=newPic))
            ranpath = random_str()
            out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('这是今天的新闻！') + '[JA]'
            voiceGenerate(tex, out)
            await bot.send(event, Voice(path=out))

    #天气查询模块
    import re
    import plugins.weatherQuery
    @bot.on(GroupMessage)
    async def weather_query(event: GroupMessage):
        # 从消息链中取出文本
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        m = re.match(r'^查询\s*(\w+)\s*$', msg.strip())
        if m:
            # 取出指令中的地名
            city = m.group(1)
            await bot.send(event, '查询中……')
            # 发送天气消息
            await bot.send(event, await plugins.weatherQuery.querys(city))


    # 对早的回复
    @bot.on(GroupMessage)
    def on_group_message(event: GroupMessage):
        if  str(event.message_chain).startswith('早') :
            if len(str(event.message_chain))<6:
                index = random.randint(1, 4)
                if index == 1:
                    ranpath = random_str()
                    out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('早上好') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 2:
                    ranpath = random_str()
                    out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[ZH]早安，天气很好呢[ZH]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 3:
                    ranpath = random_str()
                    out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('今天也要加油') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index >3:
                    ranpath = random_str()
                    out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('早上好~！，想出去走走吗？~') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))


    # 对艾特的回复
    @bot.on(GroupMessage)
    def on_group_message(event: GroupMessage):
        if At(bot.qq) in event.message_chain:
            index=random.randint(1,4)
            if index==1:
                return bot.send(event, [At(event.sender.id), ' 你在叫我吗？'])
            if index==2:
                return bot.send(event, [At(event.sender.id), ' 唉，怎么了。我做了什么奇怪的事情吗'])
            if index==3:
                return bot.send(event, [At(event.sender.id), ' 做什么呢'])

    #不准亲
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain).endswith('亲亲') :
            index = random.randint(1, 4)
            if index==1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不准亲......快走开，变态！~') + '[JA]'
                await bot.send(event,'不准亲，走开')
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\6.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你是看到谁都想亲吗.....真是奇怪的人呢~') + '[JA]'
                await bot.send(event,'你是看到谁都想亲吗.....')
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('一块钱亲一口~，怎么样!?.......很划算吧') + '[JA]'
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))

        else:
            return

    #对不对？
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if '对不对' in str(event.message_chain) :#or (('我是' in str(event.message_chain)) and str(event.message_chain).endswith('吗')):
            index = random.randint(1, 5)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('当然是了！......笨蛋！.......这还用问吗~？') + '[JA]'
                #await bot.send(event, '')
                #await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\6.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不知道呢.......或许吧....') + '[JA]'
                #await bot.send(event, '你是看到谁都想亲吗.....')
                #await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('应该是吧.....我感觉是的.....') + '[JA]'
                #await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('绝对不是.....这样绝对很奇怪啊！.....') + '[JA]'
                #await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))

        else:
            return


    #对日日的回复
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain)=='日日':
            index = random.randint(1, 11)
            if index == 1:
                await bot.send(event, [At(event.sender.id), ' 又开始了，又开始了......'])
                return bot.send(event,Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\11.jpg'))

            if index == 2:
                await bot.send(event, [At(event.sender.id), ' 唉，那个.....不行的吧！绝对不行的吧！'])
                return bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\20.jpg'))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你在想什么呢？') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\12.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==4:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[ZH]……哈~……哈~……嗯~……嗯啊~……不……不要~……咦咦咦啊啊啊啊啊啊~……[ZH]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\p2\\10.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==5:
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\9.jpg'))
                return bot.send(event, [At(event.sender.id), ' 标记了一个变态:' + str(event.sender.id)] )
            if index ==6:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('这样很有趣呢！') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\18.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==7:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不是很明白，这是什么意思呢？') + '[JA]'
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\4.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index ==8:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你想说什么呢，我在听.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\6.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==9:
                await bot.send(event, Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\2.jpg'))
                return bot.send(event, '不懂了.....这到底是什么呢')
            if index==10:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('笨蛋，变态，烦死了') + '[JA]'
                await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\9.jpg'))
                voiceGenerate(tex, out)
            if index>10:
                s=random.randint(1,20)
                si=str(s)
                return bot.send(event,Image(path=sys.argv[0][:-20]+'PythonPlugins\\plugins\\PICTURE\\haiXiu\\'+si+'.jpg'))


    #中文生成
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain).startswith('中文'):
            modelList = ['0', '1', '2', '3']
            if len(str(event.message_chain)) <280:
                if '#' in str(event.message_chain):
                    textt=str(event.message_chain).split("#")
                    if textt[1] in modelList:
                        model=int(textt[1])
                        tex = '[ZH]'+((textt[0])[2:])+'[ZH]'
                    else:
                        model=0
                        tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                else:
                    tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                    model=0
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex,out,model)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                # out = 'D:\\Mirai\\Yiris\\PythonPlugins\\plugins\\voices\\01.wav'
                tex = '[ZH]太常了哦......[ZH]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))

    #或许是功能菜单
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain)=='/help':
            index = random.randint(1, 5)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('这是所有的功能菜单') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]唉？想看我的功能菜单吗？？~真拿你没办法呢.....只准看一次哦......[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('这是什么意思呢，连我的功能都不清楚吗？......') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index > 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('稍等呀，很快就有了~') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))

    #反6工具
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain) == '6':
            index = random.randint(1, 5)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不许说6!，不可以~绝对不行！') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))
                return bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\12.jpg'))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]唉？那是什么呢，很有趣吗.....[JA]'
                voiceGenerate(tex, out)
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\3.jpg'))
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('这是什么......不是很理解.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event,'这是什么......不是很理解.....')
                await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\6.jpg'))
                return bot.send(event, Voice(path=out))
            if index > 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('说六是不可以的~') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event,'随便说六是不可以的~')
                await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                return bot.send(event, Voice(path=out))

    #日语生成
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if  str(event.message_chain).startswith('说'):
            modelList=['0','1','2','3']
            if len(str(event.message_chain)) <280:
                if '#' in str(event.message_chain):
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelList:
                        model = int(textt[1])
                        tex = '[JA]' + translate((textt[0])[1:]) + '[JA]'
                    else:
                        model = 0
                        tex = '[JA]' + translate(str(event.message_chain)[1:]) + '[JA]'
                else:
                    tex = '[JA]' + translate(str(event.message_chain)[1:]) + '[JA]'
                    model=0
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex, out,model)
                await bot.send(event,Voice(path=out))
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))

    #笑话生成
    @bot.on(GroupMessage)
    async def make_jokes(event: GroupMessage):
        if str(event.message_chain).startswith('/') and str(event.message_chain).endswith('笑话'):
            x = str(event.message_chain).strip()[1:-2]
            joke = get_joke(x)
            await bot.send(event, joke)

    #凑个cp
    @bot.on(GroupMessage)
    async def make_cp_mesg(event: GroupMessage):
        if str(event.message_chain).startswith("/cp "):
            x = str(event.message_chain).replace('/cp ', '', 1)
            x = x.split(' ')
            if len(x) != 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]发生了错误......请重新输入[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))
                return
            mesg = get_cp_mesg(x[0], x[1])
            await bot.send(event, mesg, True)

    #github禅语
    @bot.on(GroupMessage)
    async def github_zen(event: GroupMessage):
        if str(event.message_chain) == '/zen':
            try:
                zen = await get_zen()
            except:
                await bot.send(event, "获取zen失败！")
                return
            await bot.send(event, zen)

    #舔狗日记
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain) == '/舔':
            text = random.choice(pero_dog_contents).replace('*', '')
            await bot.send(event, text)

    #追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event:GroupMessage):
        if str(event.message_chain).startswith('添加群#'):
            s=str(event.message_chain).split('#')
            with open('Config\\moyu\\groups.txt', 'a') as file:
                file.write('\n'+s[1])
                file.close()
                await bot.send(event,'已追加')

        # 戳一戳
    '''@bot.on(NudgeEvent)
    async def NudgeEvent(event: NudgeEvent):
        s = ['你在想什么呢？', '不要戳了......', '检测到外部撞击', '这是什么？', '嗯？很有趣吗......', '不能理解的行为.....有什么含义吗', '戳一次十块!','别戳了，再戳就坏掉了']
        tex=random.choice(s)'''



    #抽象话
    @bot.on(GroupMessage)
    async def abstract_message_transformer(event: GroupMessage):
        if not str(event.message_chain).startswith('/抽象'):
            return
        x = str(event.message_chain).replace('/抽象', '', 1).strip()
        if x == '':
            await bot.send(event, "指令格式为'/抽象+内容',内容不能为空", True)
            return

        def get_pinyin(char: str):
            if char in pinyin:
                return pinyin[char]
            else:
                return "None"

        result = ""
        length = len(x)
        index = 0
        while index < length:
            if index < length - 1 and (get_pinyin(x[index]) + get_pinyin(x[index + 1])) in emoji:
                result += emoji[get_pinyin(x[index]) +
                                get_pinyin(x[index + 1])]
                index += 1
            elif get_pinyin(x[index]) in emoji:
                result += emoji[get_pinyin(x[index])]
            else:
                result += x[index]
            index += 1
        await bot.send(event, result, True)

    #新冠疫情数据
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain).endswith('疫情'):
            data=getCovid(str(event.message_chain)[0:-2])
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            #生成播报语音
            tex = '[JA]' + translate('查询新冠肺炎数据.......稍等哦~') + '[JA]'
            voiceGenerate(tex, out)
            await bot.send(event, Voice(path=out))
            img=['17','20','21']
            await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\'+random.choice(img)+'.jpg'))
            if data!=1:
                await bot.send(event, data)
            else:
                img1=['18','19','3']
                await bot.send(event, Image(
                    path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\' + random.choice(img1) + '.jpg'))
                await bot.send(event,'似乎没有相应的数据呢......')

    #字符画
    @bot.on(GroupMessage)
    async def charPic(event: GroupMessage):
        if str(event.message_chain).startswith('字符画'):
            '''if event.message_chain.count(Image) != 1:
                await bot.send(event, '出错啦，需要一张图片哦')
                return'''

            lst_img = event.message_chain.get(Image)
            print('已接收命令')
            await bot.send(event,'正在生成.....请稍候....')
            path=painter(lst_img[0].url)
            await bot.send(event,Image(path=path))
            #print(lst_img[0].url)




    '''#添加回复
    @bot.on(GroupMessage)
    async def addReply(event: GroupMessage):
        if str(event.message_chain).startswith('添加'):
            print(event.message_chain)
            if '#' in event.message_chain:
                stra=str(event.message_chain)
                replya=addReplys(stra)
                await bot.send(event,replya)
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你是笨蛋吗？') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, '格式似乎有问题呢.....添加格式：添加关键词#回复')
                await bot.send(event, Voice(path=out))
    #触发自定义回复
    @bot.on(GroupMessage)
    async def avvv(event: GroupMessage):
        if str(event.message_chain) in keyReply:
            replyMes=random.choice(dict.get(str(event.message_chain)))
            if len(replyMes)<40:
                ran=random.randint(0,1)
                if ran==0:
                    ranpath = random_str()
                    out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate(replyMes) + '[JA]'
                    voiceGenerate(tex, out)
                    await bot.send(event, Voice(path=out))
            else:
                await bot.send(event,replyMes)
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('删除'):
            s=dels(str(event.message_chain))
            await bot.send(event,s)'''




    #biliMonitor.main(bot)
    bot.run()