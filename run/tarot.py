# -*- coding: utf-8 -*-
import datetime
import random

from mirai import GroupMessage, Voice, At
from mirai import Image, Voice

from plugins.tarot import tarotChoice


def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| tarot module loaded successfully 已加载--- 塔罗牌 ---模块')
    @bot.on(GroupMessage)
    async def TarotGet(event: GroupMessage):
        if str(event.message_chain) == '今日塔罗' or str(event.message_chain) == '塔罗牌' or (
                ('塔罗' in event.message_chain) and (At(bot.qq) in event.message_chain)):
            side = random.randint(0, 1)
            infoBack = tarotChoice(side)
            await bot.send(event, infoBack[0])
            await bot.send(event, Image(path=infoBack[1]))