# -*- coding:utf-8 -*-
import datetime
import json

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
from mirai.models.events import BotInvitedJoinGroupRequestEvent,NewFriendRequestEvent,MemberJoinRequestEvent,MemberHonorChangeEvent,MemberCardChangeEvent

from run import MiMo, daJiao, tarot, everyDayDraw, blueArchive, musicInside, charPic, replyInside, scheduledTasks, \
    extra, wReply, voicePart, signAndDegree
def main(bot,config):

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| manager module loaded successfully 已加载--- 管理 ---模块')

    file = open('Config\\signDict.txt', 'r')
    js = file.read()
    global userdict
    userdict = json.loads(js)


    global master
    master=int(config.get('master'))

    @bot.on(GroupMessage)
    async def checkkk(event: GroupMessage):
        if str(event.message_chain)=='签到':
            file = open('Config\\signDict.txt', 'r')
            js = file.read()
            global userdict
            userdict = json.loads(js)
    @bot.on(BotInvitedJoinGroupRequestEvent)
    async def allowStranger(event: BotInvitedJoinGroupRequestEvent):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(event.from_id) in userdict.keys():
            print(time + '| 有用户记录')
            al = '同意'
            await bot.allow(event)
        else:
            print(time + '| 无用户记录')
            al = '拒绝'
        await bot.send_friend_message(master, '有新的加群申请\n来自：' + str(event.from_id) + '\n目标群：' + str(event.group_id) + '\n昵称：' + event.nick + '\n状态：' + al)


    @bot.on(NewFriendRequestEvent)
    async def allowStranger(event: NewFriendRequestEvent):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(event.from_id) in userdict.keys():
            print(time + '| 有用户记录')
            al='同意'
            await bot.allow(event)
        else:
            print(time + '| 无用户记录')
            al='拒绝'
        await bot.send_friend_message(master,'有新的好友申请\n来自：'+str(event.from_id)+'\n来自群：'+str(event.group_id)+'\n昵称：'+event.nick+'\n状态：'+al)



    @bot.on(MemberJoinRequestEvent)
    async def allowStrangerInvite(event: MemberJoinRequestEvent):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time + '| 接收入群请求')
        await bot.send_group_message(event.group_id,'有新的入群请求.....管理员快去看看吧\nQQ：'+str(event.from_id)+'\n昵称：'+event.nick+'\nextra:：'+event.message)

    @bot.on(MemberHonorChangeEvent)
    async def honorChange(event: MemberHonorChangeEvent):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time + '| 群员称号改变')
        await bot.send(event.group,event.member+'获得了称号：'+event.honor )

    @bot.on(MemberCardChangeEvent)
    async def nameChange(event: MemberCardChangeEvent):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time + '| 群员昵称改变')
        await bot.send(event.group, event.origin + ' 的昵称改成了 ' + event.current+' \n警惕新型皮套诈骗')



