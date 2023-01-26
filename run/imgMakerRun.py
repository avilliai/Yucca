import datetime

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from plugins.imgMaker import qinqin, get_user_image_url, laopo, jiehun, riyixia, warn



def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| imgMaker module loaded successfully 已加载--- 制图 ---模块')
    # 制图
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('kiss' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = qinqin(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

        elif event.message_chain.count(Image) == 1 and ('kiss' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = qinqin(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

    # 老婆
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('mywife' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = laopo(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

        elif event.message_chain.count(Image) == 1 and ('mywife' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = laopo(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

    # 结婚
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('marry' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = jiehun(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

        elif event.message_chain.count(Image) == 1 and ('marry' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = jiehun(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

    # warn
    @bot.on(GroupMessage)
    async def warns(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('warn' in event.message_chain):
            # 获取头像的url
            img_url = get_user_image_url(event.message_chain.get(At)[0].target)
            try:
                paths = warn(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

        elif event.message_chain.count(Image) == 1 and ('warn' in event.message_chain):
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = warn(img_url)
                await bot.send(event, Image(path=paths))
            except:
                print('error')

    # 日一下
    @bot.on(GroupMessage)
    async def qinqins(event: GroupMessage):
        if event.message_chain.count(At) == 1 and ('look' in event.message_chain):
            # 获取头像的url
            a = str(event.message_chain).split('#')
            a1 = a[1]
            if len(a1) > 3 or len(a1) < 1:
                await bot.send(event, 'too lang!')
            else:
                img_url = get_user_image_url(event.message_chain.get(At)[0].target)
                try:
                    paths = riyixia(img_url, a1)
                    await bot.send(event, Image(path=paths))
                except:
                    print('error')

        elif event.message_chain.count(Image) == 1 and ('look' in event.message_chain):
            a = str(event.message_chain).split('#')
            a1 = a[0]
            lst_img = event.message_chain.get(Image)
            img_url = lst_img[0].url
            try:
                paths = riyixia(img_url, a1)
                await bot.send(event, Image(path=paths))
            except:
                print('error')