# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys
import utils
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from MoeGoe import voiceGenerate
from plugins.RandomStr.RandomStr import random_str
from plugins.picGet import pic
from trans import translate
def main(bot,master):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| voiceGenerate module loaded successfully 已加载--- 语音生成 ---模块')
    # 中文生成1
    global voiceSender
    voiceSender = 0
    global voiceTrans
    voiceTrans = 0
    global modelSelect
    modelSelect=0
    global aimFriend
    aimFriend = 1840094972
    global aimGroup
    aimGroup = 699455559
    global statusPath
    statusPath = 1
    global speakerId
    speakerId = 0
    global lang
    lang = '日语'


    global modelDll
    modelDll={}
    a = os.listdir('voiceModel')
    #print(type(a))
    ind=0

    global CHOISE
    CHOISE={}

    for i in a:
        #print(i)

        if os.path.isdir('voiceModel/' + i):
            # 内层循环遍历取出模型文件
            file = os.listdir('voiceModel/' + i)
            for ass in file:
                if ass.endswith('.pth'):
                    hps_ms = utils.get_hparams_from_file('voiceModel/' + i + '/config.json')
                    speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
                    muspeakers = {}
                    for id, name in enumerate(speakers):
                        muspeakers[str(id)] = name
                        CHOISE[name]=[str(id),['voiceModel/' + i + '/' + ass,'voiceModel/' + i + '/config.json']]

                    modelDll[str(ind)]=['voiceModel/' + i + '/' + ass,'voiceModel/' + i + '/config.json',muspeakers]
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    modelSelect=['voiceModel/' + i + '/' + ass,'voiceModel/' + i + '/config.json',muspeakers]

                    print(time + '| 已读取' + 'voiceModel/' + i + '文件夹下的模型文件'+str(muspeakers))
                    ind+=1
            else:
                    pass
        else:
            pass
    #print('------\n'+str(CHOISE))

    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global speakerId
        if str(event.message_chain).startswith('中文'):
            if len(str(event.message_chain)) < 80:
                if '#' in str(event.message_chain):
                    # 获取指定的模型
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelSelect[2].keys():
                        speakerId = int(textt[1])
                    else:
                        speakerId = 0
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[ZH]' + ((textt[0])[2:]) + '[ZH]'
                    else:
                        tex = ((textt[0])[2:])
                else:
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                    else:
                        tex = (str(event.message_chain)[2:])
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 中文语音生成-----> ' + tex)

                voiceGenerate(tex, out, speakerId, modelSelect)

                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                if modelSelect[0].endswith('m.pth'):
                    tex = '[ZH]' + ('不行,太长了哦.....') + '[ZH]'
                else:
                    tex = '不行,太长了哦.....'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 中文语音生成-----> ' + tex)

                voiceGenerate(tex, out, speakerId, modelSelect)
                await bot.send(event, Voice(path=out))




    # 日语生成
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global speakerId
        if str(event.message_chain).startswith('说'):
            if len(str(event.message_chain)) < 80:
                if '#' in str(event.message_chain):
                    #获取指定的模型
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelSelect[2].keys():
                        speakerId= int(textt[1])
                    else:
                        speakerId= 0
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[JA]' + translate((textt[0])[1:]) + '[JA]'
                    else:
                        tex=translate((textt[0])[1:])
                else:
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[JA]' + translate(str(event.message_chain)[1:]) + '[JA]'
                    else:
                        tex =translate(str(event.message_chain)[1:])
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 日语语音生成-----> ' + tex)

                voiceGenerate(tex, out, speakerId,modelSelect)

                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                if modelSelect[0].endswith('m.pth'):
                    tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                else:
                    tex=translate('不行,太长了哦.....')
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 日语语音生成-----> ' + tex)

                voiceGenerate(tex, out,speakerId,modelSelect)
                await bot.send(event, Voice(path=out))


    @bot.on(GroupMessage)
    async def VoiceModelSelecter(event: GroupMessage):
        if '说' in str(event.message_chain):
            if str(event.message_chain).split('说')[0] in CHOISE.keys():
                tex=str(event.message_chain).split('说')[1]
                try:
                    tex = translate(tex)
                except:
                    tex=tex
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                speaksdfaf=int(CHOISE.get(str(event.message_chain).split('说')[0])[0])
                model=CHOISE.get(str(event.message_chain).split('说')[0])[1]
                if model[0].endswith('m.pth'):
                    tex='[JA]'+str(tex)+'[JA]'
                else:
                    pass
                voiceGenerate(tex, out, speaksdfaf, CHOISE.get(str(event.message_chain).split('说')[0])[1])
                await bot.send(event, Voice(path=out))

    @bot.on(GroupMessage)
    async def VoiceModelSelecter(event: GroupMessage):
        if '中文' in str(event.message_chain):
            if str(event.message_chain).split('中文')[0] in CHOISE.keys():
                tex = str(event.message_chain).split('中文')[1]
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                speaksdfaf = int(CHOISE.get(str(event.message_chain).split('中文')[0])[0])
                model = CHOISE.get(str(event.message_chain).split('中文')[0])[1]
                if model[0].endswith('m.pth'):
                    tex = '[ZH]' + tex + '[ZH]'
                else:
                    pass
                voiceGenerate(tex, out, speaksdfaf, CHOISE.get(str(event.message_chain).split('中文')[0])[1])
                await bot.send(event, Voice(path=out))

    @bot.on(GroupMessage)
    async def VoiceModelSelecter(event: GroupMessage):
        if str(event.message_chain)=='sp':
            tex=''
            for i in CHOISE.keys():
                tex+=i+'|'
            await bot.send(event,'可用角色如下\n'+tex)

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



    @bot.on(FriendMessage)
    async def yuYinMode(event: FriendMessage):
        if str(event.message_chain).startswith('发送'):
            global speakerId
            if lang=='中文':
                if '#' in str(event.message_chain):
                    # 获取指定的模型
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelSelect[2].keys():
                        speakerId = int(textt[1])
                    else:
                        speakerId = 0
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[ZH]' + ((textt[0])[2:]) + '[ZH]'
                    else:
                        tex = ((textt[0])[2:])
                else:
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[ZH]' + (str(event.message_chain)[2:]) + '[ZH]'
                    else:
                        tex = (str(event.message_chain)[2:])
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 中文语音生成-----> ' + tex)

                voiceGenerate(tex, out, speakerId, modelSelect)
                await bot.send_group_message(int(aimGroup), Voice(path=out))
            elif lang=='日语':
                if '#' in str(event.message_chain):
                    #获取指定的模型
                    textt = str(event.message_chain).split("#")
                    if textt[1] in modelSelect[2].keys():
                        speakerId= int(textt[1])
                    else:
                        speakerId= 0
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[JA]' + translate((textt[0])[2:]) + '[JA]'
                    else:
                        tex=translate((textt[0])[2:])
                else:
                    if modelSelect[0].endswith('m.pth'):
                        tex = '[JA]' + translate(str(event.message_chain)[1:]) + '[JA]'
                    else:
                        tex =translate(str(event.message_chain)[1:])
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(time + '| 日语语音生成-----> ' + tex)

                voiceGenerate(tex, out, speakerId,modelSelect)
                await bot.send_group_message(int(aimGroup),Voice(path=out))


    # 图片模块
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if '/pic' in str(event.message_chain):
            picNum = int((str(event.message_chain))[4:])
            if picNum < 10 and picNum > -1:
                for i in range(picNum):
                    a = pic()
                    await bot.send(event, Image(path=a))
            elif picNum == '':
                a = pic()
                await bot.send(event, Image(path=a))
            else:
                await bot.send(event, "可以发点正常的数字吗")

    # 失效
    '''@bot.on(FriendMessage)
    async def handle_group_message(event: FriendMessage):
        if str(event.message_chain).startswith('#说'):
            if len(str(event.message_chain)) < 280:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate((str(event.message_chain))[1:]) + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))
            else:
                ranpath = random_str()
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不行,太长了哦.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot(event, Voice(path=out))'''

    # 连接群
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain).startswith('连接群'):
            if str(event.sender.id)==str(master):
                sa = str(event.message_chain).split('#')
                global aimGroup
                aimGroup = int(sa[1])
                global statusPath
                statusPath = 1
                await bot.send(event, '已切换为群聊' + sa[1])
            else:
                await bot.send(event, '您不是我的管理员哦')

    # 连接群
    @bot.on(GroupMessage)
    async def on_friend_message(event: GroupMessage):
        if str(event.message_chain).startswith('连接群'):
            if str(event.sender.id) == str(master):
                sa = str(event.message_chain).split('#')
                global aimGroup
                aimGroup = int(sa[1])
                global statusPath
                statusPath = 1
                await bot.send(event, '已切换为群聊' + sa[1])
            else:
                await bot.send(event, '您不是我的管理员哦')

    # 连接人
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain).startswith('连接对象'):
            sa = str(event.message_chain).split('#')
            global aimFriend
            aimFriend = sa[1]
            global statusPath
            statusPath = 0
            await bot.send(event, '已切换为私聊对象' + sa[1])

    # 语言切换
    @bot.on(FriendMessage)
    async def Lanconfig(event: FriendMessage):
        if str(event.message_chain).startswith('切换'):
            if str(event.sender.id) == str(master):
                sa = str(event.message_chain)[2:]
                global lang
                if sa == '中文':
                    lang = sa
                    await bot.send(event, '已切换，当前使用语言' + sa)
                elif sa == '日语':
                    lang = sa
                    await bot.send(event, '已切换，当前使用语言' + sa)
                else:
                    await bot.send(event, '数值不合法，语言选择：中文/日语')
            else:
                await bot.send(event, '您不是我的管理员哦')

    # 模型切换
    @bot.on(FriendMessage)
    async def on_friend_message(event: FriendMessage):
        if str(event.message_chain).startswith('M#'):
            global modelSelect
            global speakerId
            sa = str(event.message_chain).split('#')

            if str(sa[1]) in modelDll.keys():
                modelSelect = modelDll.get(str(sa[1]))
                speakerId = 0
                await bot.send(event, '已切换，当前使用模型' + sa[1] + modelSelect[0])
                await bot.send(event, '已切换至默认音色：' + modelSelect[2].get(str(0)))
            else:
                st1 = ''
                for ass in modelDll.keys():
                    print(str(len(modelDll.keys())))
                    st1 += str(ass) + ','
                await bot.send(event, '数值不合法，可选数字：' + st1)
    # 模型切换
    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain).startswith('M#'):
            if str(event.sender.id) == str(master):
                global modelSelect
                global speakerId
                sa = str(event.message_chain).split('#')

                if str(sa[1]) in modelDll.keys():
                    modelSelect = modelDll.get(str(sa[1]))
                    speakerId=0
                    await bot.send(event, '已切换，当前使用模型' + sa[1] + modelSelect[0])
                    await bot.send(event, '已切换至默认音色：' + modelSelect[2].get(str(0)))
                else:
                    st1 = ''
                    for ass in modelDll.keys():
                        print(str(len(modelDll.keys())))
                        st1 += str(ass) + ','
                    await bot.send(event, '数值不合法，可选数字：' + st1)
            else:
                await bot.send(event, '您不是我的管理员哦')

    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        if str(event.message_chain).startswith('S#'):
            if str(event.sender.id) == str(master):
                global speakerId
                sa = str(event.message_chain).split('#')
                if str(sa[1]) in modelSelect[2].keys():
                    speakerId=sa[1]
                    await bot.send(event,'已切换至音色：'+modelSelect[2].get(str(sa[1])))
                else:
                    await bot.send(event,'当前模型'+modelSelect[0])
                    th = modelSelect[0] + ' 模型包含\n' + str(modelSelect[2]) + '\n发送 S#数字 即可切换\n'
                    await bot.send(event, th)
            else:
                await bot.send(event, '您不是我的管理员哦')



    @bot.on(GroupMessage)
    async def helpMenu(event: GroupMessage):
        if str(event.message_chain)=='voice':
            await bot.send(event,Image(path='Voice.png'))
            for i in modelDll.keys():
                value=modelDll.get(i)
                modela=i+' 号模型可选音色'+str(value[2])+'\n'
                await bot.send(event, str(modela))

                print(modela)
