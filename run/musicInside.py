# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| musicIn module loaded successfully 已加载--- 内置音频 ---模块')
    # smoke
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'smoke':
            index = random.randint(1, 6)
            if index == 0:
                out = 'plugins\\voices\\La La Run！.mp3'
                await bot.send(event, Voice(path=out))
            if index == 1:
                out = 'plugins\\voices\\smokeboy.mp3'
                await bot.send(event, Voice(path=out))
            if index == 2:
                out = 'plugins\\voices\\i got smoke.mp3'
                await bot.send(event, Voice(path=out))
            if index == 3:
                out ='plugins\\voices\\caudio.mp3'
                await bot.send(event, Voice(path=out))
            if index == 4:
                out = 'plugins\\voices\\XXX (Feat.V在燃烧).mp3'
                await bot.send(event, Voice(path=out))
            else:
                out = 'plugins\\voices\\Nayanion.mp3'
                await bot.send(event, Voice(path=out))

    # yucca唱歌
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if ('唱歌' in str(event.message_chain)) or ('情人节' in str(event.message_chain)):
            index = random.randint(1, 30)
            if index > 22:
                index = 24
                out = 'plugins\\voices\\sing\\' + str(index) + '.mp3'
            else:
                out ='plugins\\voices\\sing\\' + str(index) + '.wav'

            if ('情人节' in str(event.message_chain)):
                if index>14:
                    out = 'plugins/voices/sing/24.mp3'
                    await bot.send(event, Voice(path=out))
                    await bot.send(event, '正在播放:' + 'my heart is yours and yours alone-Moon Jelly')
                    await bot.send(event, '今天是情人节哦......来听歌吧！')
            else:
                await bot.send(event, Voice(path=out))



    # la la run
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'ba':
            # index = random.randint(1, 4)
            # if index == 0:
            out = 'plugins\\voices\\La La Run！.mp3'
            await bot.send(event, Voice(path=out))