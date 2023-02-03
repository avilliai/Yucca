# -*- coding: utf-8 -*-
import datetime
import json
import random

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

import plugins
from plugins import weatherQuery
from plugins.blueArchiveGacha import gacha
from plugins.weatherQ import weatherQ


def weather(city):
    import requests
    from plyer import notification

    """
    plyer是用来显示弹窗的模块
    安装命令：pip install plyer
    """

    params = {
        "key": "SeSI8hL-BdFhE9MKb",
        "location": city,  # 查询地点设置为访问IP所在地
        "language": "zh-Hans",
        "unit": "c",
    }

    url = "https://api.seniverse.com/v3/weather/now.json"

    # 获取数据
    r = requests.get(url, params=params)

    # 解析数据
    data = r.json()["results"]

    address = data[0]["location"]['path']  # 地点
    temperature = data[0]['now']["temperature"]  # 温度
    text = data[0]['now']["text"]  # 天气情况

    # 弹窗显示消息
    message = address + " 当前天气：\n" + \
              "温度：" + temperature + "℃" + \
              "\n天气情况：" + text + \
              "\n祝您心情愉悦！(^o^)"
    return message

    """
    标题为“当前天气”
    显示10秒钟（timeout参数）
    """
    '''notification.notify(title="当前天气",
                        message=message,
                        timeout=10)'''

def main():
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    print(time)

def picMaker():
    #批量格式化签到背景图片
    name=1
    while name<299:
        layer = Image.open('pictures/set1.png')

        bg = Image.open('pictures/backGround/' + str(name) + '.jpg')
        (x, y) = layer.size
        out = bg.resize((x, y))
        out.save('bg.png')
        bg = Image.open('bg.png')
        # merge = Image.blend(st, st2, 0.5)

        bg.paste(layer, (0, 0), layer)
        bg.save('pictures/backGround/' + str(name) + '.jpg')
        name+=1
        print('ok')

if __name__ == '__main__':
    picMaker()
