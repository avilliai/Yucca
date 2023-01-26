# -*- coding: utf-8 -*-
import datetime
import json
import random
import sys

import os
from fuzzywuzzy import fuzz,process
from mirai import Mirai, FriendMessage, WebSocketAdapter,GroupMessage
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from MoeGoe import voiceGenerate
from plugins.dictPicDown import random_str, dict_download_img
from plugins.easyReply import addReplys, dels, add
from plugins.mohuReply import mohuaddReplys, mohudels, mohuadd
from plugins.readConfig import readConfig
from plugins.superDict import importDict
from trans import translate


def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| wReply module loaded successfully 已加载--- 自定义词库 ---模块')

    file = open('Config\\dict.txt', 'r')
    js = file.read()
    global dict
    dict = json.loads(js)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| 已读取字典')

    file = open('Config\\superDict.txt', 'r')
    jss = file.read()
    global superDict
    superDict = json.loads(jss)
    global mohuKeys
    mohuKeys = superDict.keys()
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| 已读取模糊匹配字典')
    global trustUser
    trustUser = readConfig(r"Config\user.txt")
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| 已读取信任用户')

    file = open('Config\\userNamea.txt', 'r')
    js = file.read()
    global nameSet
    nameSet = json.loads(js)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| 已读取用户信息')


    #修改为你bot的名字
    global botName
    botName = 'yucca'
    #你的QQ
    global master
    master=str(1840094972)

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| ')

    #过滤词库
    global ban
    ban = ['妈', '主人', '狗', '老公', '老婆', '爸', '奶', '爷', '党', '爹', 'b', '逼', '牛', '国', '批']
    # 不回复的几率
    replypro=90

    #下面的是一堆乱七八糟的变量
    global key
    key = ''
    global value
    value = ''
    global status
    status = 0
    global sendera
    sendera = 0
    global voiceMode
    voiceMode = 0
    global delete
    delete = 0
    global mohukey
    mohukey = ''
    global mohuvalue
    mohuvalue = ''
    global mohustatus
    mohustatus = 0
    global mohusendera
    mohusendera = 0
    global mohuvoiceMode
    mohuvoiceMode = 0
    global mohudelete
    mohudelete = 0
    global delsender
    delsender = 0
    global mohudelsender
    mohudelsender = 0

    #添加语音回复详见我的另一个帖子
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
            if str(event.sender.id) in trustUser or str(event.sender.id)==master:
                global sendera
                sendera = event.sender.id
                await bot.send(event, '请输入关键词')
                global status
                status = 1
            else:
                await bot.send(event,event.sender.member_name+'没有添加的权限哦....')


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
                        path ='plugins\\voices\\' + ranpath + '.wav'
                        tex = '[JA]' + translate(str(event.message_chain)) + '[JA]'
                        voiceGenerate(tex, path)
                        value = ranpath + '.wav'
                        voiceMode=0
                    elif event.message_chain.count(Image) == 1:
                        lst_img = event.message_chain.get(Image)
                        path = lst_img[0].url
                        imgname = dict_download_img(path)
                        value = imgname
                    else:
                        value = str(event.message_chain)
                    global dict
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(time + '| 完全匹配词库添加语音-----> ' + value)
                    addStr = '添加' + key + '#' + value
                    dict = addReplys(addStr)
                    status = 0
                    await bot.send(event, '已添加至词库')


    # 模糊匹配词库管理
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '模糊语音':
            if str(event.sender.id) in trustUser or str(event.sender.id)==master:
                global mohusendera
                mohusendera = event.sender.id
                await bot.send(event, '请输入关键词')
                global mohustatus
                mohustatus = 1
                global mohuvoiceMode
                mohuvoiceMode = 1
            else:
                await bot.send(event,botName+'和您不是很熟呢....')


    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '模糊添加':
            if str(event.sender.id) in trustUser or str(event.sender.id)==master:
                global mohusendera
                mohusendera = event.sender.id
                await bot.send(event, '请输入关键词')
                global mohustatus
                mohustatus = 1
            else:
                await bot.send(event,event.sender.member_name+'没有添加的权限哦....')


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
                        path ='plugins\\voices\\' + ranpath + '.wav'
                        tex = '[JA]' + translate(str(event.message_chain)) + '[JA]'
                        voiceGenerate(tex, path)
                        value = ranpath + '.wav'
                        mohuvoiceMode=0
                    elif event.message_chain.count(Image) == 1:
                        lst_img = event.message_chain.get(Image)
                        path = lst_img[0].url
                        imgname = dict_download_img(path)
                        value = imgname
                    else:
                        value = str(event.message_chain)
                    global superDict
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(time + '| 模糊匹配词库添加语音----> ' + value)
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
        global replypro
        likeindex = 100#初始匹配相似度
        if At(bot.qq) in event.message_chain:
            getStr=str(event.message_chain).replace('@3377428814 ','')

            # 获取相似度排名
            likeindex = 70
            while likeindex > 55:
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
                            try:
                                if '{me}' in replyssssss:
                                    replyssssss = replyssssss.replace("{me}", botName)
                                else:
                                    pass
                                if 'name' in replyssssss:
                                    replyssssss = replyssssss.replace("name", str(event.sender.member_name))
                                else:
                                    pass
                                if '哥哥' in replyssssss:
                                    replyssssss = replyssssss.replace("哥哥", str(event.sender.member_name))
                                else:
                                    pass
                                if '{segment}' in replyssssss:
                                    replyssssss=replyssssss.replace("{segment}",',')
                                else:
                                    pass
                            except:
                                print('error')
                            await bot.send(event, replyssssss)
                        return
                # 没有匹配的词
                likeindex = likeindex - 1
        else:
            whetherReply = random.randint(0, 100)
            #设置回复几率
            if whetherReply > 100:
                #最低相似度
                while likeindex > 55:
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
                                    if '{name}' in replyssssss:
                                        replyssssss = replyssssss.replace("{name}", str(event.sender.member_name))
                                    else:
                                        pass
                                    if '哥哥' in replyssssss:
                                        replyssssss = replyssssss.replace("哥哥", str(event.sender.member_name))
                                    else:
                                        pass
                                    if '{segment}' in replyssssss:
                                        replyssssss = replyssssss.replace("{segment}", ',')
                                    else:
                                        pass
                                except:
                                    print('error')
                                await bot.send(event, replyssssss)
                            return
                    likeindex = likeindex - 1


    # 取消注释开放私聊
    @bot.on(FriendMessage)
    async def mohu(event: FriendMessage):
        global mohuKeys
        global superDict
        global botName
        likeindex = 99#初始匹配相似度
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
                    elif str(replyssssss).endswith('.gif'):
                        await bot.send(event, Image(path='pictures\\dictPic\\' + replyssssss))
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
            if str(event.sender.id) in trustUser:
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
            else:
                await bot.send(event,event.sender.member_name+'似乎没有删除的权限呢...')
        if str(event.message_chain).startswith('模糊删除'):
            if str(event.sender.id) in trustUser:
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
            else:
                await bot.send(event, event.sender.member_name + '似乎没有删除的权限呢...')


    # 删除回复value
    @bot.on(GroupMessage)
    async def dele(event: GroupMessage):
        if str(event.message_chain).startswith('del#'):
            if str(event.sender.id) in trustUser:
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
            else:
                await bot.send(event, event.sender.member_name + '似乎没有删除的权限呢...')
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
            if str(event.sender.id) in trustUser:
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
            else:
                await bot.send(event, event.sender.member_name + '似乎没有删除的权限呢...')

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

    # 追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event: GroupMessage):
        if str(event.message_chain).startswith('授权#'):
            if str(event.sender.id)==master:
                s = str(event.message_chain).split('#')
                with open('Config\\user.txt', 'a') as file:
                    file.write('\n' + s[1])
                await bot.send(event, '已更新受信任用户')
                global trustUser
                trustUser = readConfig(r"Config\user.txt")
            else:
                await bot.send(event,event.sender.member_name+'不是'+botName+'的master哦')

    # 追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event: GroupMessage):
        if str(event.message_chain).startswith('取消授权#'):
            if str(event.sender.id) == master:
                for i in trustUser:
                    print(i)
                s = str(event.message_chain).split('#')
                if (s[1]+'\n') in trustUser:
                    trustUser.remove(s[1]+'\n')
                elif s[1] in trustUser:
                    trustUser.remove(s[1])
                elif ('\n'+s[1]) in trustUser:
                    trustUser.remove('\n'+s[1])
                else:
                    await bot.send(event,'该用户无授权记录')
                await bot.send(event, '已更新受信任用户')
                print('-----------')
                for i in trustUser:
                    print(i)
                with open('Config\\user.txt', 'w') as file:
                    for i in trustUser:
                        file.write(i)
            else:
                await bot.send(event, event.sender.member_name + '不是' + botName + '的master哦')
    @bot.on(GroupMessage)
    async def restarts(event: GroupMessage):
        if str(event.message_chain)=='更新词库' and str(event.sender.id)==master:
            importDict(1)
            importDict(2)
            file = open('Config\\dict.txt', 'r')
            js = file.read()
            global dict
            dict = json.loads(js)
            print('已读取字典')

            file = open('Config\\superDict.txt', 'r')
            jss = file.read()
            global superDict
            superDict = json.loads(jss)
            global mohuKeys
            mohuKeys = superDict.keys()
            print('已读取模糊匹配字典')
            await bot.send(event, '已更新')

        # 设定称谓
        @bot.on(GroupMessage)
        async def setName(event: GroupMessage):
            global nameSet
            if str(event.message_chain).startswith('callMe'):
                name = str(event.message_chain)[6:]
                nameSet[str(event.sender.id)] = name
                ok = 1
                for i in ban:
                    if i in name:
                        await bot.send(event, '这样的称呼似乎不太合适呢....')
                        ok = 0
                        break
                if name == botName:
                    await bot.send(event, '可是这好像是我的名字....')
                if ok == 1:
                    await bot.send(event, '好的，接下来我会用' + name + '来称呼您.....')
                js = json.dumps(nameSet)
                file = open('Config\\userNamea.txt', 'w')
                file.write(js)
                file.close()


