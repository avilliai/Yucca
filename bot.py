# -*- coding:utf-8 -*-

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from run import MiMo, daJiao, tarot, everyDayDraw, blueArchive, musicInside, charPic, replyInside, scheduledTasks, \
    extra, wReply, voicePart

if __name__ == '__main__':
    bot = Mirai(3552663628, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))


    botName = 'yucca'
    # 菜单
    @bot.on(GroupMessage)
    async def help(event: GroupMessage):
        if '帮助' in str(event.message_chain) or '菜单' in str(event.message_chain):
            await bot.send(event, Image(path='Config\\help.png'))
            await bot.send(event, '这是' + botName + '的功能列表\nヾ(≧▽≦*)o')





    #imgMakerRun.main(bot)#制图功能
    MiMo.main(bot)#随机人设
    daJiao.main(bot)#打搅功能
    tarot.main(bot)#塔罗牌功能
    everyDayDraw.main(bot)#每日抽卡
    blueArchive.main(bot)#碧蓝档案相关
    musicInside.main(bot)#内置音频库
    charPic.main(bot)#字符画
    replyInside.main(bot)#部分内置回复
    scheduledTasks.main(bot)#定时任务
    extra.main(bot)#杂七杂八功能
    voicePart.main(bot)#语音生成（主动）
    wReply.main(bot)#自定义回复
    bot.run()