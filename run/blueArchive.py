# -*- coding: utf-8 -*-
import json
import os
import datetime
import random

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from plugins.blueArchiveGacha import gacha

import datetime
def main(bot):

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time+'| blueArchive module loaded successfully 已加载--- 碧蓝档案 ---模块')

    @bot.on(GroupMessage)
    async def baGacha(event: GroupMessage):
        times = ['一', '二', '三', '四', '五', '六', '十连', '10抽', '10连', '十抽']
        if str(event.message_chain) in times:
            #rule = 'ba(.*?)抽'
            # times = int(re.findall(rule, str(event.message_chain), re.S)[0])

            if True:

                pic = gacha(10)
                await bot.send(event, Image(path=pic))
            else:
                await bot.send(event, "数值不合法")