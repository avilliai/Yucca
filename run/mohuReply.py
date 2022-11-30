# -*- coding: utf-8 -*-
# 模糊匹配词库管理
import json
import sys
from random import random

from fuzzywuzzy import fuzz
from mirai import GroupMessage, Voice, At
from mirai import Image, Voice

from MoeGoe import voiceGenerate
from plugins.RandomStr.RandomStr import random_str
from plugins.dictPicDown import dict_download_img
from plugins.mohuReply import mohuaddReplys, mohudels
from trans import translate


def main(bot):
    file = open('Config\\superDict.txt', 'r')
    jss = file.read()
    superDict = json.loads(jss)
    mohuKeys = superDict.keys()
    print('已读取模糊匹配字典')
    mohukey = ''
    mohuvalue = ''
    mohustatus = 0
    mohusendera = 0
    mohuvoiceMode = 0
    mohudelete = 0

    #添加回复
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
                    mohustatus = 0
                    await bot.send(event, '已添加至词库')
    #触发自定义回复
    @bot.on(GroupMessage)
    async def mohu(event: GroupMessage):
        global mohuKeys
        global superDict
        if At(bot.qq) in event.message_chain:
            for i in mohuKeys:
                likeM = fuzz.partial_ratio(str(event.message_chain), i)
                if likeM > 50:
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
                            replyMes = txt.replace("{name}", str(event.sender.member_name))
                        if '{segment}' in replyMes:
                            replyMes = txt.replace("{segment}", ',')
                        await bot.send(event, replyMes)
                    return
                else:
                    continue
        else:
            whetherReply = random.randint(0, 100)
            if whetherReply > 85:
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
                                replyMes = txt.replace("{name}", str(event.sender.member_name))
                            if '{segment}' in replyMes:
                                replyMes = txt.replace("{segment}", ',')
                            await bot.send(event, replyMes)
                        return
                    else:
                        continue
            else:
                return
    #删除
    '''@bot.on(GroupMessage)
    async def delss(event: GroupMessage):
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
                await bot.send(event, '已删除关键词：' + (str(event.message_chain)[4:]))'''
