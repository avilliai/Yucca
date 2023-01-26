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
    # smoke
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'smoke':
            index = random.randint(1, 6)
            if index == 0:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\La La Run！.mp3'
                await bot.send(event, Voice(path=out))
            if index == 1:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\smokeboy.mp3'
                await bot.send(event, Voice(path=out))
            if index == 2:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\i got smoke.mp3'
                await bot.send(event, Voice(path=out))
            if index == 3:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\caudio.mp3'
                await bot.send(event, Voice(path=out))
            if index == 4:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\XXX (Feat.V在燃烧).mp3'
                await bot.send(event, Voice(path=out))
            else:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\Nayanion.mp3'
                await bot.send(event, Voice(path=out))

    # yucca唱歌
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if ('唱歌' in str(event.message_chain)):
            index = random.randint(1, 28)
            if index > 22:
                index = 23
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\sing\\' + str(index) + '.mp3'
            else:
                out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\sing\\' + str(index) + '.wav'
            await bot.send(event, Voice(path=out))

    # la la run
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == 'ba':
            # index = random.randint(1, 4)
            # if index == 0:
            out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\La La Run！.mp3'
            await bot.send(event, Voice(path=out))