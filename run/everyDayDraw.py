# -*- coding: utf-8 -*-
import json
import os
import datetime
import random

from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain



def main(bot):
    smallDict = {'大吉': 'daji.jpg', '大凶': 'daxiong.jpg', '吉': 'ji.jpg', '小吉': 'xiaoji.jpg', '小凶': 'xiaoxiong.jpg','凶': 'xiong.jpg', '中吉': 'zhongji.jpg', '中凶': 'zhongxiong.jpg','吉 ': 'ji.jpg','大吉 ': 'daji.jpg','小吉 ':'xiaoji.jpg'}
    smallDictkeys = list(smallDict.keys())

    @bot.on(GroupMessage)
    async def drawp(event: GroupMessage):

        if str(event.message_chain) == '今日运势' or str(event.message_chain) =='今日人品':
            today = str(datetime.date.today())
            exist=os.path.exists('Config\\'+today+'.txt')
            renpin=random.randint(0,100)
            if exist:
                file = open('Config\\'+today+'.txt', 'r')
                js = file.read()
                dict = json.loads(js)
                print('已读取字典')
                usera=dict.keys()
                if str(event.sender.id) in usera:
                    yunshiJI=dict.get(str(event.sender.id))
                    if str(event.message_chain) == '今日运势':
                        await bot.send(event, event.sender.member_name+'今天的运势是' + yunshiJI[0])
                        await bot.send(event, Image(path='pictures\\Atri\\' + yunshiJI[1]))
                    else:
                        await bot.send(event, event.sender.member_name+'今天的人品值是:' + yunshiJI[2])

                else:
                    yunShi = random.choice(smallDictkeys)
                    yunShiPic = smallDict.get(yunShi)
                    if str(event.message_chain) == '今日运势':
                        await bot.send(event, event.sender.member_name+'今天的运势是' + yunShi)
                        await bot.send(event, Image(path='pictures\\Atri\\' + yunShiPic))
                    else:
                        await bot.send(event, event.sender.member_name+'今天的人品值是:' + str(renpin))
                        # await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                        if renpin > 80:#如果人品值大于80
                            await bot.send(event, '意外的还不错嘛.....')
                            # await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                        elif renpin > 50:
                            await bot.send(event, '还行啦.....')
                            # await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                        elif renpin < 50:
                            await bot.send(event, '有些意外呢.....')
                            # await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                        else:
                            print('有点可怜啊.....')
                    dict[str(event.sender.id)] = [yunShi,yunShiPic,str(renpin)]
                    js = json.dumps(dict)
                    file = open('Config\\' + today + '.txt', 'w')
                    file.write(js)
                    file.close()

            else:
                dict={}
                yunShi = random.choice(smallDictkeys)
                yunShiPic = smallDict.get(yunShi)
                if str(event.message_chain) == '今日运势':
                    await bot.send(event, event.sender.member_name+'今天的运势是' + yunShi)
                    await bot.send(event, Image(path='pictures\\Atri\\' + yunShiPic))
                else:
                    await bot.send(event, event.sender.member_name+'今天的人品值是:' + str(renpin))
                    if renpin>80:
                        await bot.send(event,'意外的还不错嘛.....')
                        #await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                    elif renpin>50:
                        await bot.send(event,'还行啦.....')
                        #await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                    elif renpin<50:
                        await bot.send(event,'有些意外呢.....')
                        #await bot.send(event,Image(path=''))#你可以把想添加的图片放在path=''后面，如await bot.send(event,Image(path='D\\普通文件夹\\我可是高性能的.jpg'))
                    else:
                        print('有点可怜啊.....')
                dict[str(event.sender.id)] = [yunShi,yunShiPic,str(renpin)]
                js = json.dumps(dict)
                file = open('Config\\'+today+'.txt', 'w')
                file.write(js)
                file.close()





