# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from MoeGoe import voiceGenerate
from plugins.RandomStr.RandomStr import random_str
from trans import translate


def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| replyIn module loaded successfully 已加载--- 内置回复 ---模块')
    # 对早的回复
    @bot.on(GroupMessage)
    def on_group_message(event: GroupMessage):
        if  str(event.message_chain)=='早安' or event.message_chain=='早' or event.message_chain=='早上好':
            if len(str(event.message_chain))<6:
                index = random.randint(1, 4)
                if index == 1:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('早上好') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 2:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
                    tex = '[ZH]早安，天气很好呢[ZH]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 3:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('今天也要加油') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index >3:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
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
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不准亲......快走开，变态！~') + '[JA]'
                await bot.send(event,'这种要求的话....就这一次哦...')
                await bot.send(event,Image(path='plugins\\PICTURE\\p2\\6.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你是看到谁都想亲吗.....真是奇怪的人.....') + '[JA]'
                await bot.send(event,'你是看到谁都想亲吗.....')
                await bot.send(event,Image(path='plugins\\PICTURE\\p2\\5.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index==3:
                await bot.send(event,Image(path='plugins\\PICTURE\\p2\\13.jpg'))
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
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('当然是了！......笨蛋！.......这还用问吗~？') + '[JA]'
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不知道呢.......或许吧....') + '[JA]'

                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('应该是吧.....我感觉是的.....') + '[JA]'

                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index == 3:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('绝对不是.....这样绝对很奇怪啊！.....') + '[JA]'
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
                return bot.send(event,Image('plugins\\PICTURE\\haiXiu\\11.jpg'))

            if index == 2:
                await bot.send(event, [At(event.sender.id), ' 唉，那个.....不行的吧！绝对不行的吧！'])
                return bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\20.jpg'))
            if index == 3:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你在想什么呢？') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\12.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==4:
                ranpath = random_str()
                out ='plugins\\voices\\' + ranpath + '.wav'
                tex = '[ZH]……哈~……哈~……嗯~……嗯啊~……不……不~……咦咦咦啊啊啊啊啊啊~……[ZH]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path='plugins\\PICTURE\\p2\\10.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==5:
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\9.jpg'))
                return bot.send(event, [At(event.sender.id), ' 标记了一个变态:' + str(event.sender.id)] )
            if index ==6:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('这样很有趣呢！') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\18.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==7:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('不是很明白，这是什么意思呢？') + '[JA]'
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\4.jpg'))
                voiceGenerate(tex, out)
                return bot.send(event, Voice(path=out))
            if index ==8:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('你想说什么呢，我在听.....') + '[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Image(path='Pplugins\\PICTURE\\haiXiu\\6.jpg'))
                return bot.send(event, Voice(path=out))
            if index ==9:
                await bot.send(event, Image(path='plugins\\PICTURE\\haiXiu\\2.jpg'))
                return bot.send(event, '不懂了.....这到底是什么呢')
            if index==10:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]' + translate('笨蛋，变态，烦死了') + '[JA]'
                await bot.send(event, Image(path='plugins\\PICTURE\\p2\\9.jpg'))
                voiceGenerate(tex, out)
            if index>10:
                s=random.randint(1,20)
                si=str(s)
                return bot.send(event,Image(path='plugins\\PICTURE\\haiXiu\\'+si+'.jpg'))
        # 喜欢
        @bot.on(GroupMessage)
        async def on_group_message(event: GroupMessage):
            if (At(bot.qq) in event.message_chain) and (('老婆' in event.message_chain) or ('喜欢' in event.message_chain) or ('爱' in event.message_chain) ) :
                index = random.randint(1, 6)
                if index == 1:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('不可以的吧，说这种话绝对不行的！') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 2:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
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
                    out = 'plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate('可以的哦，......最喜欢这样了....') + '[JA]'
                    voiceGenerate(tex, out)
                    return bot.send(event, Voice(path=out))
                if index == 2:
                    ranpath = random_str()
                    out = 'plugins\\voices\\' + ranpath + '.wav'
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

