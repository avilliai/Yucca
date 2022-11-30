#-*- coding:utf-8 -*-
from mirai import GroupMessage, Voice
from mirai.models import NudgeEvent, MemberJoinEvent, MemberCardChangeEvent
import mirai

def main(bot):

    ''''@bot.on(MemberJoinEvent)
    async def join(event: MemberJoinEvent):
        await bot.send(event.member,'欢迎'+str(event.member.member_name)+'呀')'''

    @bot.on(GroupMessage)
    async def charPic(event: GroupMessage):
        if Voice in event.message_chain:
            lst_img = event.message_chain.get(Voice)
            print('已接收命令')
            await Voice.download(Voice,'test01.wav')
            path = lst_img[0].url
            print(path)

