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
def qinqin(url):
    fileName=dict_download_img(url)
    file="pictures\\dictPic\\"+fileName
    #剪切图像
    infile = file
    outfile = 'pictures/cutted.png'
    im = Image.open(infile)
    (x, y) = im.size  # read image size
    x_s = 589  # define standard width
    y_s = 577  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(outfile)
    #发起超级融合
    st = Image.open(outfile)
    st2 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\1.png")
    st3 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\2.png")
    #merge = Image.blend(st, st2, 0.5)
    st.paste(st2)
    st.paste(st3,(0,460))
    s='pictures\\imgs.png'
    st.save('pictures\\imgs.png')
    return s

def get_user_image_url(qqid):
    return f'https://q4.qlogo.cn/g?b=qq&nk={qqid}&s=640'

def laopo(url):
    fileName=dict_download_img(url)
    file="pictures\\dictPic\\"+fileName
    #剪切图像
    infile = file
    outfile = 'pictures/cutted.png'
    im = Image.open(infile)
    (x, y) = im.size  # read image size
    x_s = 420  # define standard width
    y_s = 420  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(outfile)
    #发起超级融合
    st2 = Image.open(outfile)
    st = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\3.jpg")
    #merge = Image.blend(st, st2, 0.5)
    st.paste(st2,(110,91))
    s='pictures\\imgs.png'
    st.save('pictures\\imgs.png')
    return s

def jiehun(url):
    fileName=dict_download_img(url)
    file="pictures\\dictPic\\"+fileName
    #剪切图像
    infile = file
    outfile = 'pictures/cutted.png'
    im = Image.open(infile)
    (x, y) = im.size  # read image size
    x_s = 1080  # define standard width
    y_s = 1080  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(outfile)
    #发起超级融合
    st = Image.open(outfile)
    st2 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\jiehun.png")

    im = st
    mark = st2
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (0,60))
    out = Image.composite(layer, im, layer)
    out.save('pictures\\imgs.png')
    return 'pictures\\imgs.png'

    '''st.paste(st2)
    s='pictures\\imgs.png'
    st.save('pictures\\imgs.png')
    return s'''
def riyixia(url,str):
    stra=str
    fileName=dict_download_img(url)
    file="pictures\\dictPic\\"+fileName
    #剪切图像
    infile = file
    outfile = 'pictures/cutted.png'
    im = Image.open(infile)
    (x, y) = im.size  # read image size
    x_s = 500  # define standard width
    y_s = 500  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(outfile)
    #发起超级融合
    st = Image.open(outfile)
    st2 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\5.png")

    im = st2
    mark = st
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (79,99))
    out = Image.composite(layer, im, layer)
    out.save('pictures\\imgs.png')

    font = ImageFont.truetype('D:\E\YunFengFeiYunTi\YunFengFeiYunTi\\YunFengFeiYunTi-2.ttf',40)

    # 打开底版图片
    imageFile = "pictures\\imgs.png"
    tp = Image.open(imageFile)
    if len(str)<3:
        font = ImageFont.truetype('D:\E\YunFengFeiYunTi\YunFengFeiYunTi\\YunFengFeiYunTi-2.ttf', 50)
        draw = ImageDraw.Draw(tp)
        draw.text((315, 20), stra, (12, 0, 6), font=font)
    # 在图片上添加文字 1
    else:
        draw = ImageDraw.Draw(tp)
        draw.text((310, 20), stra, (12, 0, 6), font=font)

    # 保存
    tp.save("pictures\\imgs.png")

    return 'pictures\\imgs.png'
def warn(url):
    fileName=dict_download_img(url)
    file="pictures\\dictPic\\"+fileName
    #剪切图像
    infile = file
    outfile = 'pictures/cutted.png'
    im = Image.open(infile)
    (x, y) = im.size  # read image size
    x_s = 450  # define standard width
    y_s = 450  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(outfile)
    #发起超级融合
    st = Image.open(outfile)
    st2 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\s11.png")

    im = st2
    mark = st
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (33,99))
    out = Image.composite(layer, im, layer)
    out.save('pictures\\imgs.png')

    st = Image.open('pictures\\imgs.png')
    st2 = Image.open("D:\Mirai\YirisVoiceGUI\PythonPlugins\plugins\PICTURE\\s11.png")

    im = st
    mark = st2
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (0,0))
    out = Image.composite(layer, im, layer)
    out.save('pictures\\imgs.png')

    return 'pictures\\imgs.png'


if __name__ == '__main__':
    print(warn('https://q4.qlogo.cn/g?b=qq&nk=919467430&s=640'))


