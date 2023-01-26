# -*- coding:utf-8 -*-

import json
import random
import sys
import time
#from plugins.cloudMusicCom import getCom
from fuzzywuzzy import fuzz,process
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai import Startup, Shutdown
from mirai.models import BotJoinGroupEvent, MemberCardChangeEvent
from graiax import silkcoder
from mirai.models.events import NudgeEvent

from MoeGoe import voiceGenerate, voice_conversion
# from plugins import biliMonitor, signPlugin
from plugins import manager
from plugins.Covid import getCovid
from plugins.RandomStr.RandomStr import random_str
from plugins.abstractMess import emoji, pinyin
from plugins.blueArchiveGacha import gacha
from plugins.charPicture import painter
from plugins.chatGPT import GPT
from plugins.cloudMusicCom import getCom

from plugins.cpGenerate import get_cp_mesg
from plugins.dictPicDown import dict_download_img
from plugins.easyReply import addReplys, dels, add
from plugins.gitZen import get_zen
from plugins.imgMaker import qinqin, get_user_image_url, laopo, jiehun, riyixia, warn
from plugins.jokeMaker import get_joke
from plugins.keepChating import run_conversation
from plugins.mohuReply import mohuaddReplys, mohudels, mohuadd
from plugins.moyu import moyu
from plugins.newsEveryday import news
from plugins.peroDog import pero_dog_contents
from plugins.picGet import pic
from plugins.tarot import tarotChoice
from readConfig import readConfig
from run import mohuReply, tarot, imgMakerRun, everyDayDraw, daJiao, MiMo, nodgeReply, blueArchive, musicInside
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

    file = open('Config\\userNamea.txt', 'r')
    js = file.read()
    nameSet = json.loads(js)
    print('已读取用户信息')

    severGroups=readConfig(r"Config\moyu\groups.txt")
    print('已读取服务群聊')

    botName = 'yucca'
    # 过滤词库
    ban = ['妈', '主人', '狗', '公', '婆', '爸', '奶', '爷', '党', '爹', 'b', '逼', '牛', '国', '批','男','爸']

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

    # 这里是ChatGPT的回复区
    chatSender = 0
    chatMode = 0
    elseMes = 0
    chatWant = 0


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
                await bot.send(event,'这种要求的话....就这一次哦...')
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
            if len(str(event.message_chain)) <60:
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
            if len(str(event.message_chain)) <70:
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
        if '帮助' in str(event.message_chain) or '菜单' in str(event.message_chain):
            await bot.send(event,Image(path='Config\\help.png'))
            await bot.send(event,'这是'+botName+'的功能列表\nヾ(≧▽≦*)o')


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


    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '添加语音':
            global sendera
            sendera = event.sender.id
            await bot.send(event, '请输入关键词')
            global status
            status = 1
            global voiceMode
            voiceMode = 1


    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '开始添加':
            global sendera
            sendera = event.sender.id
            await bot.send(event, '请输入关键词')
            global status
            status = 1


    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global status
        baner = 0
        global ban
        if status == 1:
            if event.sender.id == sendera:
                global key
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    key = str(lst_img[0].url)
                    print(key)
                    await bot.send(event, '已记录关键词,请发送回复')
                    status = 2
                else:
                    for i in ban:
                        if i in event.message_chain:
                            await bot.send(event, '似乎是不合适的词呢.....')
                            baner = 1
                            status = 0
                    if baner != 1:
                        key = str(event.message_chain)
                        await bot.send(event, '已记录关键词,请发送回复')
                        status = 2


    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global status
        global ban
        if status == 2:
            global key
            global voiceMode
            baner = 0
            if event.sender.id == sendera:
                for i in ban:
                    if i in event.message_chain:
                        await bot.send(event, '似乎是不合适的词呢.....')
                        baner = 1
                        key = ''
                        status = 0
                if baner != 1:
                    # 语音生成详见另一个帖子,配置成功后取消此行注释
                    if voiceMode == 1:
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
                    global dict
                    addStr = '添加' + key + '#' + value
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
        global ban
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
        global ban
        if mohustatus == 2:
            global mohukey
            global mohuvoiceMode
            global mohusendera
            baner = 0
            if event.sender.id == mohusendera:
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
                    mohuKeys = superDict.keys()
                    mohustatus = 0
                    await bot.send(event, '已添加至词库')


    # 完全匹配词库回复
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global dict
        if event.message_chain.count(Image) == 1:
            lst_img = event.message_chain.get(Image)
            dictkey = str(lst_img[0].url)
            if dictkey in dict.keys():
                try:
                    replyMes = random.choice(dict.get(str(dictkey)))
                except:
                    return
                try:
                    if str(replyMes).endswith('.png'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + replyMes))
                    elif str(replyMes).endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
                    else:
                        await bot.send(event, replyMes)
                except:
                    print('回复模块----->error')
            else:
                return
        if str(event.message_chain) in dict.keys():
            try:
                replyMes = random.choice(dict.get(str(event.message_chain)))
            except:
                return
            try:
                if str(replyMes).endswith('.png'):
                    await bot.send(event, Image(path='pictures\\dictPic\\' + replyMes))
                elif str(replyMes).endswith('.wav'):
                    await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
                else:
                    await bot.send(event, replyMes)
            except:
                print('回复模块----->error')
        else:
            return


    # 模糊词库触发回复
    @bot.on(GroupMessage)
    async def mohu(event: GroupMessage):
        global mohuKeys
        global superDict
        global botName
        global user
        likeindex = 100  # 初始匹配相似度
        if At(bot.qq) in event.message_chain:
            getStr = str(event.message_chain).replace('@3377428814 ', '')
            # 获取相似度排名
            #likeindex = 99
            while likeindex > 45:
                for i in mohuKeys:
                    # 获取本次循环中消息和词库相似度，用相似度作为key
                    likeM = fuzz.partial_ratio(getStr, i)
                    # 如果大于本次循环设置阈值则发送消息
                    if likeM > likeindex or likeM == likeindex:
                        superRep = superDict.get(i)
                        replyssssss = random.choice(superRep)
                        if str(replyssssss).endswith('.png'):
                            await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                        elif str(replyssssss).endswith('.wav'):
                            await bot.send(event, Voice(path='plugins\\voices\\' + replyssssss))
                        elif str(replyssssss).endswith('.gif'):
                            await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                        else:
                            if '{me}' in replyssssss:
                                replyssssss = replyssssss.replace("{me}", botName)
                            else:
                                pass
                            if 'name' in replyssssss:
                                if str(event.sender.id) in nameSet.keys():
                                    replyssssss = replyssssss.replace("name", nameSet.get(str(event.sender.id)))
                                else:
                                    replyssssss = replyssssss.replace("name", str(event.sender.member_name))
                            else:
                                pass
                            if '哥哥' in replyssssss:
                                if str(event.sender.id) in nameSet.keys():
                                    replyssssss = replyssssss.replace("哥哥", nameSet.get(str(event.sender.id)))
                                else:
                                    replyssssss = replyssssss.replace("哥哥", str(event.sender.member_name))
                            else:
                                pass
                            if '您' in replyssssss:
                                if str(event.sender.id) in nameSet.keys():
                                    replyssssss = replyssssss.replace("您", nameSet.get(str(event.sender.id)))
                                else:
                                    replyssssss = replyssssss.replace("您", str(event.sender.member_name))
                            else:
                                pass
                            if '{segment}' in replyssssss:
                                replyssssss = replyssssss.replace("{segment}", ',')
                            else:
                                pass
                            sas=random.randint(0,5)
                            if sas==1 or sas==2:
                                ranpath = random_str()
                                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                                if sas==1:
                                    if botName in replyssssss:
                                        replyssssss = replyssssss.replace(botName, '我')
                                    else:
                                        pass
                                    tex = '[JA]' + translate(replyssssss) + '[JA]'
                                else:

                                    tex = '[ZH]' + replyssssss + '[ZH]'
                                voiceGenerate(tex, out)
                                await bot.send(event,Voice(path=out))
                            else:
                                await bot.send(event, replyssssss)
                        return
                # 没有匹配的词
                likeindex = likeindex - 1
        else:
            whetherReply = random.randint(0, 100)
            # 设置回复几率
            if whetherReply > 900:
                # 最低相似度
                while likeindex > 75:
                    for i in mohuKeys:
                        # 获取本次循环中消息和词库相似度，用相似度作为key
                        likeM = fuzz.partial_ratio(str(event.message_chain), i)
                        # 如果大于本次循环设置阈值则输出，结束循环
                        if likeM > likeindex or likeM == likeindex:
                            superRep = superDict.get(i)
                            replyssssss = random.choice(superRep)
                            if str(replyssssss).endswith('.png'):
                                await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                            elif str(replyssssss).endswith('.wav'):
                                await bot.send(event, Voice(path='plugins\\voices\\' + replyssssss))
                            elif str(replyssssss).endswith('.gif'):
                                await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                            else:
                                try:
                                    if '{me}' in replyssssss:
                                        replyssssss = replyssssss.replace("{me}", botName)
                                    else:
                                        pass
                                    if 'name' in replyssssss:
                                        if str(event.sender.id) in nameSet.keys():
                                            replyssssss = replyssssss.replace("name", nameSet.get(str(event.sender.id)))
                                        else:
                                            replyssssss = replyssssss.replace("name", str(event.sender.member_name))
                                    else:
                                        pass
                                    if '哥哥' in replyssssss:
                                        if str(event.sender.id) in nameSet.keys():
                                            replyssssss = replyssssss.replace("哥哥", nameSet.get(str(event.sender.id)))
                                        else:
                                            replyssssss = replyssssss.replace("哥哥", str(event.sender.member_name))
                                    else:
                                        pass
                                    if '您' in replyssssss:
                                        if str(event.sender.id) in nameSet.keys():
                                            replyssssss = replyssssss.replace("您", nameSet.get(str(event.sender.id)))
                                        else:
                                            replyssssss = replyssssss.replace("您", str(event.sender.member_name))
                                    else:
                                        pass
                                    if '{segment}' in replyssssss:
                                        replyssssss = replyssssss.replace("{segment}", ',')
                                    else:
                                        pass
                                except:
                                    print('error')
                                sas = random.randint(0, 3)
                                if sas == 1 or sas == 2:
                                    ranpath = random_str()
                                    out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                                    if sas == 1:
                                        if botName in replyssssss:
                                            replyssssss = replyssssss.replace(botName, '我')
                                        else:
                                            pass
                                        tex = '[JA]' + translate(replyssssss) + '[JA]'
                                    else:
                                        tex = '[ZH]' + replyssssss + '[ZH]'
                                    voiceGenerate(tex, out)
                                    await bot.send(event, Voice(path=out))
                                else:
                                    await bot.send(event, replyssssss)
                            return
                    likeindex = likeindex - 1


    # 取消注释开放私聊
    @bot.on(FriendMessage)
    async def mohu(event: FriendMessage):
        global mohuKeys
        global superDict
        global botName
        likeindex = 99  # 初始匹配相似度
        # 获取相似度排名
        while likeindex > 55:
            for i in mohuKeys:
                # 获取本次循环中消息和词库相似度，用相似度作为key
                likeM = fuzz.partial_ratio(str(event.message_chain), i)
                # 如果大于本次循环设置阈值则发送消息
                if likeM > likeindex or likeM == likeindex:
                    superRep = superDict.get(i)
                    replyssssss = random.choice(superRep)
                    if str(replyssssss).endswith('.png'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
                    elif str(replyssssss).endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + replyssssss))
                    else:
                        if '{me}' in replyssssss:
                            replyssssss = replyssssss.replace("{me}", botName)
                        else:
                            pass
                        if 'name' in replyssssss:
                            replyssssss = replyssssss.replace("name", str(event.sender.get_name()))
                        else:
                            pass
                        if '哥哥' in replyssssss:
                            replyssssss = replyssssss.replace("哥哥", str(event.sender.get_name()))
                        else:
                            pass
                        if '{segment}' in replyssssss:
                            replyssssss = replyssssss.replace("{segment}", ',')
                        else:
                            pass
                        await bot.send(event, replyssssss)
                    return
            # 没有匹配的词
            likeindex = likeindex - 1

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
                    key = str(event.message_chain)
                s = dels(key)
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
                    key = str(event.message_chain)
                s = mohudels(key)
                global superDict
                superDict = s
                await bot.send(event, '已删除关键词：' + (str(event.message_chain)[4:]))
                global mohuKeys
                mohuKeys = superDict.keys()
            except:
                pass

    # 删除回复value
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('del#'):
            s1 = str(event.message_chain).split('#')
            aimStr = s1[1]
            global dict
            if aimStr in dict.keys():
                replyMes = dict.get(aimStr)
                number = 0
                for i in replyMes:
                    await bot.send(event, '编号:' + str(number))
                    number += 1
                    if i.endswith('.png'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + i))
                    elif i.endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + i))
                    else:
                        await bot.send(event, i)
                global delete
                global delsender
                global key
                key = aimStr
                delsender = event.sender.id
                delete = 1
                await bot.send(event, '请发送要删除的序号')
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
                    dict = add(key, replyMes)
                    delete = 0
                    await bot.send(event, '已删除')
                except:
                    delete = 0
                    await bot.send(event, '下标不合法')

    # 删除模糊回复value
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('Mel#'):
            s1 = str(event.message_chain).split('#')
            aimStr = s1[1]
            global superDict
            if aimStr in superDict.keys():
                replyMes = superDict.get(aimStr)
                number = 0
                for i in replyMes:
                    await bot.send(event, '编号:' + str(number))
                    number += 1
                    if i.endswith('.png'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + i))
                    elif i.endswith('.wav'):
                        await bot.send(event, Voice(path='plugins\\voices\\' + i))
                    else:
                        await bot.send(event, i)
                global mohudelete
                global mohudelsender
                global mohukey
                mohukey = aimStr
                mohudelsender = event.sender.id
                mohudelete = 1
                await bot.send(event, '请发送要删除的序号')
    # 删除指定下标执行部分
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global mohudelete
        global mohudelsender
        global superDict
        if mohudelete == 1:
            if event.sender.id == mohudelsender:
                global mohukey
                replyMes = superDict.get(mohukey)
                try:
                    del replyMes[int(str(event.message_chain))]
                    superDict = mohuadd(mohukey, replyMes)
                    mohudelete = 0
                    await bot.send(event, '已删除')
                except:
                    mohudelete = 0
                    await bot.send(event, '下标不合法')
    ''''@bot.on(GroupMessage)
    async def gptGene(event: GroupMessage):
        if str(event.message_chain).startswith('/g') or str(event.message_chain).startswith('chat'):
            if str(event.message_chain).startswith('/gt'):
                a = str(event.message_chain)[3:]
                print('即将发送' + a)
                backst = GPT(a,0)
                print('已返回')
                if len(backst)>500:
                    asf=cut(backst,500)
                    for i in asf:
                        await bot.send(event,i)
                else:
                    await bot.send(event,backst)
            else:
                if str(event.message_chain).startswith('chat'):
                    a=str(event.message_chain)[4:]
                else:
                    a=str(event.message_chain)[2:]
                print('即将发送'+a)
                backst=GPT(a)
                print('已返回')

                await bot.send(event,Image(path=backst))


    def cut(obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatWant
        global userDict
        if str(event.message_chain).startswith('开始聊天'):
            if chatMode != 0:
                chatWant += 1
                await bot.send(event, '稍等哦，我正在为别人解决问题....')

            else:
                global chatSender
                chatSender = event.sender.id
                
                await bot.send(event, '好的....' + event.sender.member_name + '想问什么呢...')
                chatMode = 1
                if event.sender.id not in userDict.keys():
                    userDict[event.sender.id] = []


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatSender
        global elseMes
        global userDict
        global chatWant
        if event.sender.id == chatSender:
            if chatMode == 1:
                if 'stop' in str(event.message_chain):
                    chatMode = 0
                    chatSender = 0
                    elseMes = 0
                    chatWant = 0
                    await bot.send(event, '本次对话记录已保存，和' + event.sender.member_name + '聊天很开心...')
                else:
                    conversation = userDict.get(event.sender.id)
                    print('已接收' + str(event.message_chain))
                    conversation.append(str(event.message_chain))
                    cona = "\n".join(conversation)
                    reply = mains(cona)
                    if len(reply) > 6:
                        step = 5
                        str1 = ''
                        reply = [reply[i:i + step] for i in range(0, len(reply), step)]
                        new = []
                        for sa in reply:
                            for saa in sa:
                                str1 += (saa + '\n')
                            new.append(str1)
                        reply = new

                    for i in reply:
                        i = i.replace('Assistant', 'yucca')
                        await bot.send(event, i)
                    # reply=reply.replace('Assistant','yucca')
                    # await bot.send(event,reply)
                    userDict[event.sender.id] = conversation
                    # await bot.send(event, reply[4:])
                    elseMes += 1

        else:
            elseMes += 1


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatSender
        global elseMes
        global chatWant
        global userDict
        if elseMes > 100 or chatWant > 1:
            await bot.send(event, '已记录当前聊天数据')

            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
        if event.sender.id == chatSender and event.message_chain == 'stop':
            await bot.send(event, '已记录本次聊天数据')

            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
            await bot.send(event, '那我.....先离开啦~')'''
    # 设定称谓
    @bot.on(GroupMessage)
    async def setName(event: GroupMessage):
        global nameSet
        if str(event.message_chain).startswith('callMe'):
            name=str(event.message_chain)[6:]
            nameSet[str(event.sender.id)]=name
            ok=1
            for i in ban:
                if i in name:
                    await bot.send(event, '这样的称呼似乎不太合适呢....')
                    ok=0
                    break
            if name==botName:
                await bot.send(event,'可是这好像是我的名字....')
            if ok==1:
                await bot.send(event,'好的，接下来我会用'+name+'来称呼您.....')
            js = json.dumps(nameSet)
            file = open('Config\\userNamea.txt', 'w')
            file.write(js)
            file.close()
    # 网易云
    @bot.on(GroupMessage)
    async def cloudmusicComm(event: GroupMessage):
        if '到点了' in  str(event.message_chain) or ('网易云' in str(event.message_chain)):
            time.sleep(3)
            cosfm=getCom()
            await bot.send(event,str(cosfm))



    #imgMakerRun.main(bot)#制图功能
    MiMo.main(bot)#随机人设
    daJiao.main(bot)#打搅功能
    tarot.main(bot)#塔罗牌功能
    everyDayDraw.main(bot)#每日抽卡
    blueArchive.main(bot)#碧蓝档案相关
    musicInside.main(bot)#内置音频库
    bot.run()