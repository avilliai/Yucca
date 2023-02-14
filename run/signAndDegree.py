# -*- coding: utf-8 -*-
import json
import os
import datetime
import random
import time
import sys
from PIL import Image
from mirai import Image as Im
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

import plugins
from plugins.imgMaker import get_user_image_url
from plugins.weatherQ import weatherQ
import cv2
from PIL.ImageDraw import ImageDraw
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from mirai import GroupMessage, At
from mirai.models import Image as mImage
from plugins.RandomStr.RandomStr import random_str
from plugins.dictPicDown import dict_download_img
from PIL import Image
import cv2
import numpy as np

def main(bot):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + '| signAndWeather module loaded successfully 已加载--- 天气与签到 ---模块')

    file = open('Config\\signDict.txt', 'r')
    js = file.read()
    global userdict
    userdict = json.loads(js)


    global newUser
    newUser={}

    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        if '签到' ==str(event.message_chain):
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 接收签到任务')
            if str(event.sender.id) in userdict.keys():
                data=userdict.get(str(event.sender.id))
                signOrNot = data.get('ok')
                time114514 = str(datetime.datetime.now().strftime('%Y-%m-%d'))
                if signOrNot!=time114514:
                    imgurl=get_user_image_url(event.sender.id)
                    fileName = dict_download_img(imgurl)
                    file = "pictures\\dictPic\\" + fileName
                    touxiang=Image.open(file)
                    fad = touxiang.resize((450, 450), Image.ANTIALIAS)
                    fad.save('pictures/touxiang.png')


                    city = data.get('city')
                    startTime = data.get('st')
                    times = str(int(data.get('sts')) + 1)
                    if times=='6':
                        await bot.send(event,'词库自动授权完成,发送 开始添加 试试吧',True)
                    exp = str(int(data.get('exp')) + random.randint(1, 20))
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    id = data.get('id')
                    data['sts'] = times
                    data['exp'] = exp
                    data['ok'] = time114514
                    userdict[str(event.sender.id)] = data
                    newData = json.dumps(userdict)
                    with open('Config\\signDict.txt', 'w') as fp:
                        fp.write(newData)

                    weather = weatherQ(city)

                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(time + '| 正在制作签到图片')

                    layer = Image.open('pictures/touxiang.png')
                    name = random.randint(2, 298)
                    bg = Image.open('pictures/backGround/' + str(name) + '.jpg')
                    # merge = Image.blend(st, st2, 0.5)

                    bg.paste(layer, (120, 147))

                    bg.save('pictures/imgsa.png')

                    imageFile = "pictures\\imgsa.png"
                    tp = Image.open(imageFile)
                    font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 110)
                    draw = ImageDraw.Draw(tp)
                    draw.text((423, 773), id, (12, 0, 6), font=font)
                    font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 73)
                    draw.text((2000, 716), weather, (12, 0, 6), font=font)
                    draw.text((509, 1100), nowTime, (12, 0, 6), font=font)
                    draw.text((509, 1258), times, (12, 0, 6), font=font)
                    draw.text((509, 1419), '当前exp:' + exp, (12, 0, 6), font=font)
                    draw.text((1395, 1208), startTime, (12, 0, 6), font=font)

                    tp.save("pictures\\imgsa.png")
                    await bot.send(event, Im(path="pictures\\imgsa.png"),True)
                else:
                    await bot.send(event,'不要重复签到！笨蛋！',True)
            else:
                await bot.send(event,'请完善用户信息,发送  注册#城市名 以完善您的城市信息\n例如  注册#通辽',True)
                global newUser
                newUser[str(event.sender.id)]=0

    @bot.on(GroupMessage)
    async def handle_group_message(event: GroupMessage):
        global newUser
        if str(event.sender.id) in newUser.keys():
            newUser.pop(str(event.sender.id))
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 用户＋1')
            time114514 = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            try:
                city = str(event.message_chain).split('#')[1]
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                await bot.send(event, '正在验证城市......，')
                weather = weatherQ(city)
                await bot.send(event, '成功')
            except:
                await bot.send(event,'error，默认执行 注册#通辽 ,随后可发送 修改城市#城市名 进行地区修改')
                city='通辽'
                weather = weatherQ(city)
            global userdict
            userdict[str(event.sender.id)] = {"city": city, "st": time, "sts": "1", "exp": "0",
                                              "id": str(len(userdict.keys())+1),'ok':time114514}
            data = userdict.get(str(event.sender.id))

            imgurl = get_user_image_url(event.sender.id)
            fileName = dict_download_img(imgurl)
            file = "pictures\\dictPic\\" + fileName
            touxiang = Image.open(file)
            fad = touxiang.resize((450, 450), Image.ANTIALIAS)
            fad.save('pictures/touxiang.png')
            city = data.get('city')
            startTime = data.get('st')
            times = str(int(data.get('sts')) + 1)
            exp = str(int(data.get('exp')) + random.randint(1, 20))
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = data.get('id')
            data['sts'] = times
            data['exp'] = exp
            userdict[str(event.sender.id)] = data
            newData = json.dumps(userdict)
            with open('Config\\signDict.txt', 'w') as fp:
                fp.write(newData)


            layer = Image.open('pictures/touxiang.png')
            name = random.randint(2, 298)
            bg = Image.open('pictures/backGround/' + str(name) + '.jpg')
            # merge = Image.blend(st, st2, 0.5)

            bg.paste(layer, (120, 147))

            bg.save('pictures/imgsa.png')

            imageFile = "pictures\\imgsa.png"
            tp = Image.open(imageFile)
            font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 110)
            draw = ImageDraw.Draw(tp)
            draw.text((423, 773), id, (12, 0, 6), font=font)
            font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 73)
            draw.text((2000, 716), weather, (12, 0, 6), font=font)
            draw.text((509, 1100), nowTime, (12, 0, 6), font=font)
            draw.text((509, 1258), times, (12, 0, 6), font=font)
            draw.text((509, 1419), '当前exp:' + exp, (12, 0, 6), font=font)
            draw.text((1395, 1208), startTime, (12, 0, 6), font=font)

            tp.save("pictures\\imgsa.png")
            await bot.send(event,Im(path="pictures\\imgsa.png"),True)
    @bot.on(GroupMessage)
    async def changeCity(event: GroupMessage):
        if str(event.message_chain).startswith('修改城市#'):
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(time + '| 接收城市修改请求')
            city=str(event.message_chain)[5:]
            try:

                data=userdict.get(str(event.sender.id))
                await bot.send(event, '正在验证城市......，')
                weather = weatherQ(city)
                data['city']=city
                await bot.send(event, '成功')
                userdict[str(event.sender.id)] = data
                newData = json.dumps(userdict)
                with open('Config\\signDict.txt', 'w') as fp:
                    fp.write(newData)

            except:
                await bot.send(event,'没有对应的城市数据......，',True)

            data = userdict.get(str(event.sender.id))

            imgurl = get_user_image_url(event.sender.id)
            fileName = dict_download_img(imgurl)
            file = "pictures\\dictPic\\" + fileName
            touxiang = Image.open(file)
            fad=touxiang.resize((450, 450), Image.ANTIALIAS)
            fad.save('pictures/touxiang.png')

            city = data.get('city')
            weather = weatherQ(city)
            startTime = data.get('st')
            times = str(int(data.get('sts')) + 0)
            exp = str(int(data.get('exp')) +0)
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = data.get('id')


            layer = Image.open('pictures/touxiang.png')
            name = random.randint(2, 298)
            bg = Image.open('pictures/backGround/' + str(name) + '.jpg')
            # merge = Image.blend(st, st2, 0.5)

            bg.paste(layer, (120, 147))

            bg.save('pictures/imgsa.png')

            imageFile = "pictures\\imgsa.png"
            tp = Image.open(imageFile)
            font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 110)
            draw = ImageDraw.Draw(tp)
            draw.text((423, 773), id, (12, 0, 6), font=font)
            font = ImageFont.truetype('Config/H-TTF-BuMing-B-2.ttf', 73)
            draw.text((2000, 716), weather, (12, 0, 6), font=font)
            draw.text((509, 1100), nowTime, (12, 0, 6), font=font)
            draw.text((509, 1258), times, (12, 0, 6), font=font)
            draw.text((509, 1419), '当前exp:' + exp, (12, 0, 6), font=font)
            draw.text((1395, 1208), startTime, (12, 0, 6), font=font)

            tp.save("pictures\\imgsa.png")
            await bot.send(event, Im(path="pictures\\imgsa.png"),True)










