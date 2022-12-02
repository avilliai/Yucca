# -*- coding:utf-8 -*-

import json
import random
import sys
import time

from fuzzywuzzy import fuzz,process
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai import Startup, Shutdown
from mirai.models import BotJoinGroupEvent, MemberCardChangeEvent
from graiax import silkcoder
from MoeGoe import voiceGenerate, voice_conversion
# from plugins import biliMonitor, signPlugin
from plugins import manager
from plugins.Covid import getCovid
from plugins.RandomStr.RandomStr import random_str
from plugins.abstractMess import emoji, pinyin
from plugins.charPicture import painter
from plugins.cpGenerate import get_cp_mesg
from plugins.dictPicDown import dict_download_img
from plugins.easyReply import addReplys, dels, add
from plugins.gitZen import get_zen
from plugins.imgMaker import qinqin, get_user_image_url, laopo, jiehun, riyixia, warn
from plugins.jokeMaker import get_joke
from plugins.mohuReply import mohuaddReplys, mohudels
from plugins.moyu import moyu
from plugins.newsEveryday import news
from plugins.peroDog import pero_dog_contents
from plugins.picGet import pic
from plugins.tarot import tarotChoice
from readConfig import readConfig
from run import mohuReply, tarot, imgMakerRun
from trans import translate

if __name__ == '__main__':
    bot = Mirai(3552663628, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')

    file = open('Config\\superDict.txt', 'r')
    jss = file.read()
    superDict = json.loads(jss)
    mohuKeys=superDict.keys()
    print('已读取模糊匹配字典')



    severGroups=readConfig(r"Config\moyu\groups.txt")
    print('已读取服务群聊')

    key=''
    value=''
    status=0
    sendera=0
    voiceMode=0
    delete=0

    mohukey = ''
    mohuvalue = ''
    mohustatus = 0
    mohusendera = 0
    mohuvoiceMode = 0
    mohudelete = 0

    delsender=0
    zifuhua=0

    voiceSender=0
    voiceTrans=0
    # 私聊内容
    '''@bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain) == '你好':
            await bot.send(event, 'Hello World!')'''

    # 监听群聊消息
    @bot.on(BotJoinGroupEvent)
    async def tests():
        await bot.send_friend_message(1840094972,'新加入了'+str(BotJoinGroupEvent.group.id))



            # print(str(event.message_chain))  # 打印消息内容

    # 图片模块
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        # if str(event.message_chain) == '/pic':
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

    # 这里是定时任务区
    # 定时摸鱼,可以在Config//moyu//中添加群
    scheduler = AsyncIOScheduler()
    @bot.on(Startup)
    def start_scheduler(_):
        scheduler.start()  # 启动定时器
        print('当前路径' + sys.argv[0])
        Path=sys.argv[0][:-20]
    @bot.on(Shutdown)
    def stop_scheduler(_):
        scheduler.shutdown(True)  # 结束定时器
    # 摸鱼人日历
    @scheduler.scheduled_job(CronTrigger(hour=16, minute=50))
    async def timer():
        moyuPic=moyu()
        global severGroups
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
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('啊......好累呢，该下班了') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]到下班时间了......晚上去哪里玩呢?...[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('辛苦了，要注意休息哦。') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))
            if index > 3:
                ranpath = random_str()
                out = sys.argv[0][:-20]+'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('今天也好好努力过了......今天也很棒了') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send_group_message(intTrans, Voice(path=out))


    # 早八新闻自动推送
    @scheduler.scheduled_job(CronTrigger(hour=7, minute=40))
    async def timer():
        newsPic = news()
        global severGroups
        for i in severGroups:
            intTrans = int(i)
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
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
        for i in severGroups:
            intTrans = int(i)
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
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

    # 早八新闻
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

    # 天气查询
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
        if  str(event.message_chain)=='早安' or event.message_chain=='早' or event.message_chain=='早上好':
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

    # 不准亲
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if ('亲亲' in event.message_chain) and (At(bot.qq) in event.message_chain) :
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
                tex = '[JA]' + translate('你是看到谁都想亲吗.....真是奇怪的人.....') + '[JA]'
                await bot.send(event,'你是看到谁都想亲吗.....')
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==3:
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                return bot.send(event, '一块钱亲一下~，怎么样!?.......很划算吧')
            else:
                return bot.send(event,Image(path='plugins\\PICTURE\\p2\\22.jpg'))


    # 对不对？
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if '对不对' in str(event.message_chain) :# or (('我是' in str(event.message_chain)) and str(event.message_chain).endswith('吗')):
            index = random.randint(1, 5)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('当然是了！......笨蛋！.......这还用问吗~？') + '[JA]'
                # await bot.send(event, '')
                # await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\6.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不知道呢.......或许吧....') + '[JA]'
                # await bot.send(event, '你是看到谁都想亲吗.....')
                # await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('应该是吧.....我感觉是的.....') + '[JA]'
                # await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('绝对不是.....这样绝对很奇怪啊！.....') + '[JA]'
                # await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))

        else:
            return


    # 对日日的回复
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if ((('日日' in event.message_chain) or ('透' in event.message_chain) ) and (At(bot.qq) in event.message_chain)):
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
                tex = '[ZH]……哈~……哈~……嗯~……嗯啊~……不……不~……咦咦咦啊啊啊啊啊啊~……[ZH]'
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


    # 中文生成
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

    # 喜欢
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if (At(bot.qq) in event.message_chain) and (('老婆' in event.message_chain) or ('喜欢' in event.message_chain) or ('爱' in event.message_chain) ) :
            index = random.randint(1, 6)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不可以的吧，说这种话绝对不行的！') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]'+translate('真拿你没办法呢.....只准一次哦......')+'[JA]'
                voiceGenerate(tex, out)
                await bot.send(event,Image(path='plugins\\PICTURE\\haiXiu\\5.jpg'))
                return bot.send(event, Voice(path=out))
            if index == 3:
                await bot.send(event,'果然是个变态......随便就把这种话说出来了.....\n看来没办法了呢')
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\114.jpg'))
            if index ==4:
                await bot.send(event, '哦，知道了')
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\16.jpg'))
            else:
                await bot.send(event,Image(path='plugins\\PICTURE\\haiXiu\\22.jpg'))


    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if (At(bot.qq) in event.message_chain) and (('抱' in event.message_chain) or ('摸' in event.message_chain)):
            index = random.randint(1, 6)
            if index == 1:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('可以的哦，......最喜欢这样了....') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('真拿你没办法呢.....只准一次哦......') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\5.jpg'))
                return bot.send(event, Voice(path=out))
            if index == 3:
                await bot.send(event, '果然是个变态......随便就把这种话说出来了.....\n看来没办法了呢')
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\21.png'))
            if index == 4:
                await bot.send(event, '哦，知道了')
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\16.jpg'))
            else:
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\22.jpg'))

    # 日语生成
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
    #语音转换
    @bot.on(GroupMessage)
    async def voiceTan(event: GroupMessage):
        if str(event.message_chain)=='语音转换':
            global voiceSender
            voiceSender=event.sender.id
            global voiceTrans
            voiceTrans=2
            await bot.send(event,'请发送语音')

    # 语音转化附件
    @bot.on(GroupMessage)
    async def voicetransa(event: GroupMessage):
        global voiceSender
        global voiceTrans
        if event.message_chain.count(Voice):
            if voiceTrans == 2:
                if voiceSender == event.sender.id:
                    s = event.message_chain.get(Voice)
                    await Voice.download(s[0], 'plugins/voices/sing/rest.silk')
                    silkcoder.decode("plugins/voices/sing/rest.silk", "plugins/voices/sing/rest.wav",
                                     ffmpeg_para=["-ar", "44100"])
                    print('over')
                    paths = voice_conversion("plugins/voices/sing/rest.wav")
                    await bot.send(event, Voice(path=paths))
                    voiceSender = 0
                    voiceTrans = 0



    # 好友日语生成,因腾讯版本更新再不可用
    '''@bot.on(FriendMessage)
    async def handle_group_message(event: FriendMessage):
        if str(event.message_chain).startswith('说'):
            modelList = ['0', '1', '2', '3']
            if len(str(event.message_chain)) < 280:
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
                    model = 0
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex, out, model)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))'''

    # 笑话生成
    @bot.on(GroupMessage)
    async def make_jokes(event: GroupMessage):
        if str(event.message_chain).startswith('/') and str(event.message_chain).endswith('笑话'):
            x = str(event.message_chain).strip()[1:-2]
            joke = get_joke(x)
            await bot.send(event, joke)

    # 凑个cp
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

    # github禅语
    @bot.on(GroupMessage)
    async def github_zen(event: GroupMessage):
        if str(event.message_chain) == '/zen':
            try:
                zen = await get_zen()
            except:
                await bot.send(event, "获取zen失败！")
                return
            await bot.send(event, zen)

    # 舔狗日记
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain) == '/舔':
            text = random.choice(pero_dog_contents).replace('*', '')
            await bot.send(event, text)

    # 追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event:GroupMessage):
        if str(event.message_chain).startswith('添加群#'):
            s=str(event.message_chain).split('#')
            with open('Config\\moyu\\groups.txt', 'a') as file:
                file.write('\n'+s[1])
                await bot.send(event,'已追加')

        # 戳一戳


    # 菜单
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        if '帮助' in event.message_chain:
            await bot.send(event,Image(path='Config\\help.png'))
            await bot.send(event,'这是yucca的功能列表\nヾ(≧▽≦*)o')


    # 抽象话
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

    # 新冠疫情数据
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain).endswith('疫情'):
            data=getCovid(str(event.message_chain)[0:-2])
            # ranpath = random_str()
            # out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            # 生成播报语音
            # tex = '[JA]' + translate('查询新冠肺炎数据.......稍等哦~') + '[JA]'
            # voiceGenerate(tex, out)
            await bot.send(event, '查询新冠肺炎数据.......稍等哦~')
            img=['17','20','21']
            await bot.send(event, Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\'+random.choice(img)+'.jpg'))
            if data!=1:
                await bot.send(event, data)
            else:
                img1=['18','19','3']
                await bot.send(event, Image(
                    path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\' + random.choice(img1) + '.jpg'))
                await bot.send(event,'似乎没有相应的数据呢......')

    # 字符画
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

    # smoke
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'smoke':
            index=random.randint(1,4)
            if index==0:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\La La Run！.mp3'
                await bot.send(event, Voice(path=out))
            if index==1:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\smokeboy.mp3'
                await bot.send(event, Voice(path=out))
            if index==2:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\i got smoke.mp3'
                await bot.send(event, Voice(path=out))
            if index==2:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\caudio.mp3'
                await bot.send(event, Voice(path=out))
            if index>3:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\XXX (Feat.V在燃烧).mp3'
                await bot.send(event, Voice(path=out))

    # yucca唱歌
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'yucca唱歌':
            index = random.randint(1, 28)
            if index>22:
                index=23
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\sing\\' + str(index) + '.mp3'
            else:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\sing\\'+str(index)+'.wav'
            await bot.send(event, Voice(path=out))
    # la la run
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'ba':
            #index = random.randint(1, 4)
            #if index == 0:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\La La Run！.mp3'
                await bot.send(event, Voice(path=out))

    # 添加回复
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '添加语音':
            global sendera
            sendera = event.sender.id
            await bot.send(event, '请输入关键词')
            global status
            status = 1
            global voiceMode
            voiceMode=1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '开始添加':
            global sendera
            sendera=event.sender.id
            await bot.send(event,'请输入关键词')
            global status
            status = 1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global status
        baner=0
        if status==1:
            if event.sender.id==sendera:
                global key
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    key = str(lst_img[0].url)
                    print(key)
                    await bot.send(event, '已记录关键词,请发送回复')
                    status = 2
                else:
                    ban = ['妈', '主人', '狗', '老公', '老婆', '爸', '奶', '爷', '党', '爹', 'b', '逼','牛','国','批']
                    for i in ban:
                        if i in event.message_chain:
                            await bot.send(event, '似乎是不合适的词呢.....')
                            baner = 1
                            status = 0
                    if baner != 1:
                        key=str(event.message_chain)
                        await bot.send(event, '已记录关键词,请发送回复')
                        status = 2
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global status
        if status==2:
            global key
            global voiceMode
            baner=0
            if event.sender.id == sendera:
                ban=['妈','主人','狗','老公','老婆','爸','奶','爷','党','爹','b','逼','牛','国','批']
                for i in ban:
                    if i in event.message_chain:
                        await bot.send(event,'似乎是不合适的词呢.....')
                        baner=1
                        key=''
                        status=0
                if baner!=1:
                    if voiceMode==1:
                        ranpath = random_str()
                        path = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                        tex = '[JA]' + translate(str(event.message_chain)) + '[JA]'
                        voiceGenerate(tex, path)
                        value=ranpath+'.wav'
                    elif event.message_chain.count(Image) == 1:
                        lst_img = event.message_chain.get(Image)
                        path = lst_img[0].url
                        imgname = dict_download_img(path)
                        value =imgname
                    else:
                        value = str(event.message_chain)
                    global dict
                    addStr='添加'+key+'#'+value
                    dict = addReplys(addStr)
                    status = 0
                    await bot.send(event, '已添加至词库')
    # 模糊匹配词库管理
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '模糊语音':
            global mohusendera
            mohusendera = event.sender.id
            await bot.send(event, '请输入关键词')
            global mohustatus
            mohustatus = 1
            global mohuvoiceMode
            mohuvoiceMode = 1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '模糊添加':
            global mohusendera
            mohusendera = event.sender.id
            await bot.send(event, '请输入关键词')
            global mohustatus
            mohustatus = 1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global mohustatus
        baner = 0
        if mohustatus == 1:
            if event.sender.id == mohusendera:
                global mohukey
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    mohukey = str(lst_img[0].url)
                    print(mohukey)
                    await bot.send(event, '已记录关键词,请发送回复')
                    mohustatus = 2
                else:
                    ban = ['妈', '主人', '狗', '老公', '老婆', '爸', '奶', '爷', '党', '爹', 'b', '逼', '牛', '国', '批']
                    for i in ban:
                        if i in event.message_chain:
                            await bot.send(event, '似乎是不合适的词呢.....')
                            baner = 1
                            mohustatus = 0
                    if baner != 1:
                        mohukey = str(event.message_chain)
                        await bot.send(event, '已记录关键词,请发送回复')
                        mohustatus = 2
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global mohustatus
        if mohustatus == 2:
            global mohukey
            global mohuvoiceMode
            global mohusendera
            baner = 0
            if event.sender.id == mohusendera:
                ban = ['妈', '主人', '狗', '老公', '老婆', '爸', '奶', '爷', '党', '爹', 'b', '逼', '牛', '国', '批']
                for i in ban:
                    if i in event.message_chain:
                        await bot.send(event, '似乎是不合适的词呢.....')
                        baner = 1
                        mohukey = ''
                        mohustatus = 0
                if baner != 1:
                    if mohuvoiceMode == 1:
                        ranpath = random_str()
                        path = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                        tex = '[JA]' + translate(str(event.message_chain)) + '[JA]'
                        voiceGenerate(tex, path)
                        value = ranpath + '.wav'
                    elif event.message_chain.count(Image) == 1:
                        lst_img = event.message_chain.get(Image)
                        path = lst_img[0].url
                        imgname = dict_download_img(path)
                        value = imgname
                    else:
                        value = str(event.message_chain)
                    global superDict
                    addStr = '添加' + mohukey + '#' + value
                    superDict = mohuaddReplys(addStr)
                    global mohuKeys
                    mohuKeys=superDict.keys()
                    mohustatus = 0
                    await bot.send(event, '已添加至词库')


    # 触发自定义回复
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global dict
        if event.message_chain.count(Image) == 1:
            lst_img = event.message_chain.get(Image)
            dictkey = str(lst_img[0].url)
            if dictkey in dict.keys():
                try:
                    replyMes=random.choice(dict.get(str(dictkey)))
                except:
                    return
                try:
                    if str(replyMes).endswith('.png'):
                        await bot.send(event,Image(path='pictures\\dictPic\\'+replyMes))
                    elif str(replyMes).endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
                    else:
                        await bot.send(event,replyMes)
                except:
                    print('回复模块----->error')
            else:
                return
        if str(event.message_chain) in dict.keys():
            try:
                replyMes=random.choice(dict.get(str(event.message_chain)))
            except:
                return
            try:
                if str(replyMes).endswith('.png'):
                    await bot.send(event,Image(path='pictures\\dictPic\\'+replyMes))
                elif str(replyMes).endswith('.wav'):
                    await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
                else:
                    await bot.send(event,replyMes)
            except:
                print('回复模块----->error')
        else:
            return
    #模糊词库
    @bot.on(GroupMessage)
    async def mohu(event: GroupMessage):
        global mohuKeys
        global superDict
        likeindex=99
        if At(bot.qq) in event.message_chain:
            #获取相似度排名
            likeindex = 70
            while likeindex>50:
                for i in mohuKeys:
                    #获取本次循环中消息和词库相似度，用相似度作为key
                    likeM=fuzz.partial_ratio(str(event.message_chain),i)
                    #如果大于本次循环设置阈值则发送消息
                    if likeM>likeindex or likeM==likeindex:
                        superRep=superDict.get(i)
                        replyssssss=random.choice(superRep)
                        if str(replyssssss).endswith('.png'):
                            await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                        elif str(replyssssss).endswith('.wav'):
                            await bot.send(event, Voice(path='plugins\\voices\\' + replyssssss))
                        else:
                            txt = replyssssss
                            if 'name' in replyssssss:
                                replyssssss = txt.replace("name", str(event.sender.member_name))
                            await bot.send(event, replyssssss)
                        return
                #没有匹配的词
                likeindex = likeindex - 1


        else:
            whetherReply=random.randint(0,100)
            if whetherReply>85:
                while likeindex > 70:
                    for i in mohuKeys:
                        # 获取本次循环中消息和词库相似度，用相似度作为key
                        likeM = fuzz.partial_ratio(str(event.message_chain), i)
                        # 如果大于本次循环设置阈值
                        if likeM > likeindex or likeM == likeindex:
                            superRep = superDict.get(i)
                            replyssssss = random.choice(superRep)
                            if str(replyssssss).endswith('.png'):
                                await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                            elif str(replyssssss).endswith('.wav'):
                                await bot.send(event, Voice(path='plugins\\voices\\' + replyssssss))
                            else:
                                txt = replyssssss
                                if 'name' in replyssssss:
                                    replyssssss = txt.replace("name", str(event.sender.member_name))
                                await bot.send(event, replyssssss)
                            return
                    likeindex = likeindex - 1

    #私聊
    ''''@bot.on(FriendMessage)
    async def mohu(event: FriendMessage):
        global mohuKeys
        global superDict
        for i in mohuKeys:
            likeM = fuzz.partial_ratio(str(event.message_chain), i)
            if likeM > 80:
                try:
                    replyMes = random.choice(superDict.get(i))
                except:
                    return
                if str(replyMes).endswith('.png'):
                    await bot.send(event, Image(path='pictures\\dictPic\\' + replyMes))
                elif str(replyMes).endswith('.wav'):
                    await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
                else:
                    txt = replyMes
                    if '{name}' in replyMes:
                        replyMes = txt.replace("{name}", str(event.sender.get_name()))
                    if '{segment}' in replyMes:
                        replyMes = txt.replace("{segment}", ',')
                    await bot.send(event, replyMes)
                return
            else:
                continue'''


    # 删除关键字和回复
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('删除'):
            # 调用词库删除函数
            try:
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    key = lst_img[0].url
                else:
                    key=str(event.message_chain)
                s=dels(key)
                global dict
                dict = s
                await bot.send(event, '已删除关键词：' + (str(event.message_chain)[2:]))
            except:
                pass
        if str(event.message_chain).startswith('模糊删除'):
            # 调用词库删除函数
            try:
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    key = lst_img[0].url
                else:
                    key=str(event.message_chain)
                s=mohudels(key)
                global superDict
                superDict = s
                await bot.send(event, '已删除关键词：' + (str(event.message_chain)[4:]))
                global mohuKeys
                mohuKeys=superDict.keys()
            except:
                pass
    #删除回复value
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('del#'):
            s1=str(event.message_chain).split('#')
            aimStr=s1[1]
            global dict
            if aimStr in dict.keys():
                replyMes = dict.get(aimStr)
                number = 0
                for i in replyMes:
                    await bot.send(event,'编号:'+str(number))
                    number+=1
                    if i.endswith('.png'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + i))
                    elif i.endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + i))
                    else:
                        await bot.send(event, i)
                global delete
                global delsender
                global key
                key=aimStr
                delsender=event.sender.id
                delete=1
                await bot.send(event,'请发送要删除的序号')
    # 删除指定下标执行部分
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global delete
        global delsender
        global dict
        if delete == 1:
            if event.sender.id == delsender:
                global key
                replyMes = dict.get(key)
                try:
                    del replyMes[int(str(event.message_chain))]
                    dict=add(key,replyMes)
                    delete=0
                    await bot.send(event, '已删除')
                except:
                    delete =0
                    await bot.send(event,'下标不合法')

    imgMakerRun.main(bot)#制图功能
    tarot.main(bot)#塔罗牌功能
    bot.run()