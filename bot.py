# -*- coding:utf-8 -*-
import datetime
import json

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, GroupMessage
from mirai.models import BotInvitedJoinGroupRequestEvent,NewFriendRequestEvent

from run import MiMo, daJiao, tarot, everyDayDraw, blueArchive, musicInside, charPic, replyInside, scheduledTasks, \
    extra, wReply, voicePart, signAndDegree, addManager1

if __name__ == '__main__':
    with open('config.json','r',encoding='utf-8') as fp:
        data=fp.read()
    config=json.loads(data)
    qq=int(config.get('botQQ'))
    key=config.get("vertify_key")
    port= int(config.get("port"))
    bot = Mirai(qq, adapter=WebSocketAdapter(
        verify_key=key, host='localhost', port=port
    ))


    botName = config.get('botName')
    master=int(config.get('master'))

    def loadUser():
        file = open('Config/moyu/groups.txt', 'r')
        js = file.read()
        severGroupsa = json.loads(js)
        severGroups = severGroupsa.keys()

        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time1 + '| 已读取服务群聊:'+str(len(severGroupsa))+'个')

        file = open('Config\\signDict.txt', 'r')
        js = file.read()
        userdict = json.loads(js)
        userCount=userdict.keys()
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time1 + '| 已读取有记录用户:' + str(len(userCount)) + '个')

        # 修改为你bot的名字
        botName = config.get('botName')
        # 你的QQ
        master = config.get('master')
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time1 + '| botName:'+botName+'     |     master:'+master)
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time1 + '| 功能已加载完毕，正在连接mirai-api-http(如出现WARNING可忽略)')
    # 菜单
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        if '帮助' in str(event.message_chain) or '菜单' in str(event.message_chain):
            await bot.send(event, Image(path='Config\\help.png'))
            await bot.send(event, '这是' + botName + '的功能列表\nヾ(≧▽≦*)o')









    '''@bot.on(GroupMessage)
    async def help(event: GroupMessage):
        if '签到' in str(event.message_chain):
            await bot.send(event, Image(path="pictures\\imgsa.png"))'''


    def startVer():
        file_object = open("./mylog.log")
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        print(all_the_text)



    # imgMakerRun.main(bot)# 制图功能
    MiMo.main(bot)# 随机人设
    daJiao.main(bot)# 打搅功能
    tarot.main(bot)# 塔罗牌功能
    everyDayDraw.main(bot)# 每日抽卡
    blueArchive.main(bot)# 碧蓝档案相关
    musicInside.main(bot)# 内置音频库
    charPic.main(bot)# 字符画
    # replyInside.main(bot)# 部分内置回复,不要打开，会变得不幸
    scheduledTasks.main(bot)# 定时任务
    extra.main(bot)# 杂七杂八功能
    voicePart.main(bot,master)# 语音生成（主动）
    wReply.main(bot,config)# 自定义回复
    signAndDegree.main(bot)
    addManager1.main(bot,config)
    startVer()
    loadUser()
    bot.run()