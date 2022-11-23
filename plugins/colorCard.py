# -*- coding:utf-8 -*-
from PIL import Image
from functools import cmp_to_key

pic_path = r'D:\Mirai\YirisVoiceGUI\PythonPlugins\pictures\a1adaXa9aEa_a$a.jpg'
img = Image.open(pic_path)
img = img.convert('RGB')   # 修改颜色通道为RGB
x, y = img.size   # 获得长和宽

d = {}
# 提取图片中的颜色
for i in range(x):
    for k in range(y):
        color = img.getpixel((i, k))
        # Luminosity算法计算灰度值
        color_weight = color[0]*0.299 + color[1]*0.587 + color[2]*0.114
        d[color_weight] = color

# 定义一个图片用于存储颜色
color_img = Image.new('RGB', (len(d), 200), 'black')

x1 = -1
for k in sorted(d):
    x1 = x1 + 1;
    for y1 in range(0,200):
        color_img.putpixel((x1, y1), d[k])

color_img.show()
