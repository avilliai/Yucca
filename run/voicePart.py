# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys

from graiax import silkcoder
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from MoeGoe import voiceGenerate, voice_conversion
from plugins.RandomStr.RandomStr import random_str
from trans import translate
def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| voiceGenerate module loaded successfully 已加载--- 语音生成 ---模块')
    # 中文生成
    global voiceSender
    voiceSender = 0
    global voiceTrans
    voiceTrans = 0

    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain).startswith('中文'):
            modelList = ['0', '1', '2', '3']
            if len(str(event.message_chain)) < 60:
                if '#' in str(event.message_chain):
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelList:
                        model = int(textt[1])
                        tex = '[ZH]' + ((textt[0])[2:]) + '[ZH]'
                    else:
                        model = 0
                        tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                else:
                    tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                    model = 0
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex, out, model)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[ZH]太常了哦......[ZH]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))

    # 日语生成
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain).startswith('说'):
            modelList = ['0', '1', '2', '3']
            if len(str(event.message_chain)) < 70:
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
                out ='plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex, out, model)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))

    # 语音转换
    '''@bot.on(GroupMessage)
    async def voiceTan(event: GroupMessage):
        if str(event.message_chain) == '语音转换':
            global voiceSender
            voiceSender = event.sender.id
            global voiceTrans
            voiceTrans = 2
            await bot.send(event, '请发送语音')

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
                    voiceTrans = 0'''

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
                out ='PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                voiceGenerate(tex, out, model)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))'''

