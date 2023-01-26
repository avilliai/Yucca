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
from plugins.Covid import getCovid
from plugins.RandomStr.RandomStr import random_str
from plugins.abstractMess import pinyin, emoji
from plugins.cloudMusicCom import getCom
from plugins.cpGenerate import get_cp_mesg
from plugins.gitZen import get_zen
from plugins.jokeMaker import get_joke
from plugins.moyu import moyu
from plugins.newsEveryday import news
from plugins.peroDog import pero_dog_contents
from plugins.picGet import pic
from trans import translate


def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| jokeMaker module loaded successfully 已加载--- 笑话生成 ---模块')
    print(time + '| cpCreate module loaded successfully 已加载--- cp生成 ---模块')
    print(time + '| githubZen module loaded successfully 已加载--- github禅语 ---模块')
    print(time + '| peroDog module loaded successfully 已加载--- 舔狗日记 ---模块')
    print(time + '| abstract module loaded successfully 已加载--- 抽象话 ---模块')
    print(time + '| covidQuery module loaded successfully 已加载--- 疫情查询 ---模块')
    print(time + '| cloudEmo module loaded successfully 已加载--- 网易云EMO ---模块')
    print(time + '| picGet module loaded successfully 已加载--- 壁纸 ---模块')
    print(time + '| moyu module loaded successfully 已加载--- 摸鱼人日历 ---模块')
    print(time + '| news module loaded successfully 已加载--- 早八新闻 ---模块')
    print(time + '| weather module loaded successfully 已加载--- 天气查询 ---模块')
    # 笑话生成
    @bot.on(GroupMessage)
    async def make_jokes(event: GroupMessage):
        if str(event.message_chain).startswith('/') and str(event.message_chain).endswith('笑话'):
            x = str(event.message_chain).strip()[1:-2]
            joke = get_joke(x)
            await bot.send(event, joke)

    # 凑个cp
    @bot.on(GroupMessage)
    async def make_cp_mesg(event: GroupMessage):
        if str(event.message_chain).startswith("/cp "):
            x = str(event.message_chain).replace('/cp ', '', 1)
            x = x.split(' ')
            if len(x) != 2:
                ranpath = random_str()
                out = 'plugins\\voices\\' + ranpath + '.wav'
                tex = '[JA]发生了错误......请重新输入[JA]'
                voiceGenerate(tex, out)
                await bot.send(event, Voice(path=out))
                return
            mesg = get_cp_mesg(x[0], x[1])
            await bot.send(event, mesg, True)

    # github禅语
    @bot.on(GroupMessage)
    async def github_zen(event: GroupMessage):
        if str(event.message_chain) == '/zen':
            try:
                zen = await get_zen()
            except:
                await bot.send(event, "获取zen失败！")
                return
            await bot.send(event, zen)

    # 舔狗日记
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain) == '/舔':
            text = random.choice(pero_dog_contents).replace('*', '')
            await bot.send(event, text)

    # 追加推送群聊
    @bot.on(GroupMessage)
    async def addGroup(event: GroupMessage):
        if str(event.message_chain).startswith('添加群#'):
            s = str(event.message_chain).split('#')
            with open('Config\\moyu\\groups.txt', 'a') as file:
                file.write('\n' + s[1])
                await bot.send(event, '已追加')



    # 抽象话
    @bot.on(GroupMessage)
    async def abstract_message_transformer(event: GroupMessage):
        if not str(event.message_chain).startswith('/抽象'):
            return
        x = str(event.message_chain).replace('/抽象', '', 1).strip()
        if x == '':
            await bot.send(event, "指令格式为'/抽象+内容',内容不能为空", True)
            return

        def get_pinyin(char: str):
            if char in pinyin:
                return pinyin[char]
            else:
                return "None"

        result = ""
        length = len(x)
        index = 0
        while index < length:
            if index < length - 1 and (get_pinyin(x[index]) + get_pinyin(x[index + 1])) in emoji:
                result += emoji[get_pinyin(x[index]) +
                                get_pinyin(x[index + 1])]
                index += 1
            elif get_pinyin(x[index]) in emoji:
                result += emoji[get_pinyin(x[index])]
            else:
                result += x[index]
            index += 1
        await bot.send(event, result, True)

    # 新冠疫情数据
    @bot.on(GroupMessage)
    async def pero_dog(event: GroupMessage):
        if str(event.message_chain).endswith('疫情'):
            data = getCovid(str(event.message_chain)[0:-2])

            await bot.send(event, '查询新冠肺炎数据.......稍等哦~')
            img = ['17', '20', '21']
            await bot.send(event, Image(
                path='plugins\\PICTURE\\p2\\' + random.choice(img) + '.jpg'))
            if data != 1:
                await bot.send(event, data)
            else:
                img1 = ['18', '19', '3']
                await bot.send(event, Image(
                    path='plugins\\PICTURE\\p2\\' + random.choice(img1) + '.jpg'))
                await bot.send(event, '似乎没有相应的数据呢......')

    # 网易云
    @bot.on(GroupMessage)
    async def cloudmusicComm(event: GroupMessage):
        if '到点了' in str(event.message_chain) or ('网易云' in str(event.message_chain)):
            time.sleep(3)
            cosfm = getCom()
            await bot.send(event, str(cosfm))

    # 图片模块
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        # if str(event.message_chain) == '/pic':
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

    # 摸鱼
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '摸鱼':
            moyus = moyu()
            await bot.send(event, Image(path=moyus))

    # 早八新闻
    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if str(event.message_chain) == '新闻':
            newPic = news()
            await bot.send(event, Image(path=newPic))
            ranpath = random_str()
            out = 'plugins\\voices\\' + ranpath + '.wav'
            tex = '[JA]' + translate('这是今天的新闻！') + '[JA]'
            voiceGenerate(tex, out)
            await bot.send(event, Voice(path=out))

    # 天气查询
    import re
    import plugins.weatherQuery
    @bot.on(GroupMessage)
    async def weather_query(event: GroupMessage):
        # 从消息链中取出文本
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        m = re.match(r'^查询\s*(\w+)\s*$', msg.strip())
        if m:
            # 取出指令中的地名
            city = m.group(1)
            await bot.send(event, '查询中……')
            # 发送天气消息
            await bot.send(event, await plugins.weatherQuery.querys(city))