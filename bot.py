import json
import random
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai import Startup, Shutdown

from MoeGoe import voiceGenerate
# from plugins import biliMonitor, signPlugin
from plugins.Covid import getCovid
from plugins.RandomStr.RandomStr import random_str
from plugins.abstractMess import emoji, pinyin
from plugins.charPicture import painter
from plugins.cpGenerate import get_cp_mesg
from plugins.dictPicDown import dict_download_img
from plugins.easyReply import addReplys, dels
from plugins.gitZen import get_zen
from plugins.imgMaker import qinqin, get_user_image_url, laopo, jiehun
from plugins.jokeMaker import get_joke
from plugins.moyu import moyu
from plugins.newsEveryday import news
from plugins.peroDog import pero_dog_contents
from plugins.picGet import pic
from readConfig import readConfig
from trans import translate

if __name__ == '__main__':
    bot = Mirai(3552663628, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))
    #翻字典
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    key=''
    value=''
    status=0
    sender=0
    voiceMode=0
    #私聊内容
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain) == '你好':
            await bot.send(event, 'Hello World!')

    #监听群聊消息
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):#定义方法
        if str(event.message_chain) == 'test':#event.message_chain是群友发的消息，每条都监听
            await bot.send_group_message(event, 'yucca测试版YIRIS启动成功！')#向消息来源发送消息

            # print(str(event.message_chain))  # 打印消息内容

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
                tex = '[JA]到下班时间了......[JA]'
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


    #早八新闻自动推送
    @scheduler.scheduled_job(CronTrigger(hour=7, minute=40))
    async def timer():
        newsPic = news()
        txt = r"Config\moyu\groups.txt"
        groupList = readConfig(txt)
        for i in groupList:
            intTrans = int(i)
            ranpath = random_str()
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('早上好~........已经为您整理好了今天的新闻！.......有什么有趣的事情吗?') + '[JA]'
            voiceGenerate(tex, out)
            try:
                await bot.send_group_message(intTrans, Image(path=newsPic))
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                print('没有对应的群')

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
            try:
                await bot.send_group_message(intTrans, zen)
                await bot.send_group_message(intTrans, Voice(path=out))
            except:
                print('没有对应的群')

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

    #天气查询
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

    #不准亲
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
                tex = '[JA]' + translate('你是看到谁都想亲吗.....真是奇怪的人呢~') + '[JA]'
                await bot.send(event,'你是看到谁都想亲吗.....')
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==3:
                await bot.send(event,Image(path=sys.argv[0][:-20] + 'PythonPlugins\\plugins\\PICTURE\\p2\\13.jpg'))
                return bot.send(event, '一块钱亲一下~，怎么样!?.......很划算吧')
            else:
                return bot.send(event,Image(path='plugins\\PICTURE\\p2\\22.jpg'))


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
        if str(event.message_chain)=='日日' or ((('日日' in event.message_chain) or ('透' in event.message_chain) ) and (At(bot.qq) in event.message_chain)):
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

    #喜欢
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if (At(bot.qq) in event.message_chain) and (('老婆' in event.message_chain) or ('喜欢' in event.message_chain)) :
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
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\21.png'))
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
                tex = '[JA]' + translate('可以的哦......最喜欢这样了....') + '[JA]'
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
    #反6工具
    '''@bot.on(GroupMessage)
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
                return bot.send(event, Voice(path=out))'''

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
                await bot.send(event,'已追加')

        # 戳一戳


    #菜单
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        if '帮助' in event.message_chain:
            await bot.send(event,Image(path='Config\\help.png'))
            await bot.send(event,'这是yucca的功能列表\nヾ(≧▽≦*)o')


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
            #ranpath = random_str()
            #out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
            #生成播报语音
            #tex = '[JA]' + translate('查询新冠肺炎数据.......稍等哦~') + '[JA]'
            #voiceGenerate(tex, out)
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

    #字符画
    @bot.on(GroupMessage)
    async def charPic(event: GroupMessage):
        if str(event.message_chain).startswith('字符画'):
            lst_img = event.message_chain.get(Image)
            print('已接收命令')
            await bot.send(event,'正在生成.....请稍候....')
            path=painter(lst_img[0].url)
            await bot.send(event,Image(path=path))
            #print(lst_img[0].url)

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
            if index>2:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\XXX (Feat.V在燃烧).mp3'
                await bot.send(event, Voice(path=out))

    #la la run
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'ba':
            #index = random.randint(1, 4)
            #if index == 0:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\La La Run！.mp3'
                await bot.send(event, Voice(path=out))

    #添加回复
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '添加语音':
            global sender
            sender = event.sender.id
            await bot.send(event, '请输入关键词')
            global status
            status = 1
            global voiceMode
            voiceMode=1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '开始添加':
            global sender
            sender=event.sender.id
            await bot.send(event,'请输入关键词')
            global status
            status = 1
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global status
        if status==1:
            if event.sender.id==sender:
                global key
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
            if event.sender.id == sender:
                ban=['妈','主人','狗','老公','老婆','爸','奶','爷','党']
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

    #自定义词库的废案
    '''@bot.on(GroupMessage)
    async def addReply(event: GroupMessage):
        if str(event.message_chain).startswith('添加'):
            print(event.message_chain)
            if '#' in event.message_chain:
                if event.message_chain.count(Image) == 1:
                    lst_img = event.message_chain.get(Image)
                    path = lst_img[0].url
                    imgname=dict_download_img(path)
                    aaa=str(event.message_chain).split('#')
                    stra=aaa[0]+'#'+imgname
                else:
                    stra=str(event.message_chain)
                #更新全局变量：词库
                global dict
                dict=addReplys(stra)
                await bot.send(event,'添加完成')
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你是笨蛋吗？') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, '格式似乎有问题呢.....添加格式：添加关键词#回复')
                await bot.send(event, Voice(path=out))'''
    #触发自定义回复
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global dict
        if str(event.message_chain) in dict.keys():
            replyMes=random.choice(dict.get(str(event.message_chain)))
            if str(replyMes).endswith('.png'):
                await bot.send(event,Image(path='pictures\\dictPic\\'+replyMes))
            elif str(replyMes).endswith('.wav'):
                await bot.send(event, Voice(path='plugins\\voices\\' + replyMes))
            else:
                await bot.send(event,replyMes)
    #删除关键字
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('删除'):
            #调用词库删除函数
            try:
                s=dels(str(event.message_chain))
            except:
                pass
            global dict
            dict=s
            await bot.send(event,'已删除关键词：'+(str(event.message_chain)[2:]))
    #制图
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At)==1 and ('kiss' in event.message_chain):
            #获取头像的url
            img_url=get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = qinqin(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))
        elif event.message_chain.count(Image)==1 and ('kiss' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = qinqin(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))

    #老婆
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('mywife' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = laopo(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))
        elif event.message_chain.count(Image) == 1 and ('mywife' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = laopo(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))

    #结婚
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('marry' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = jiehun(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))
        elif event.message_chain.count(Image) == 1 and ('marry' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = jiehun(img_url)
            except:
                print('error')
            await bot.send(event, Image(path=paths))
    #biliMonitor.main(bot)
    #signPlugin.main(bot)
    bot.run()