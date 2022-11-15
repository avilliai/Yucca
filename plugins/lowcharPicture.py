# coding: utf8
from PIL import Image # PIL 是一个 Python 图像处理库

from plugins.imgDownload import imgDown

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
# 是我们的字符画所使用的字符集，一共有 70 个字符，字符的种类与数量可以自己根据字符画的效果反复调试的

WIDTH = 100 # 字符画的宽
HEIGHT = 120 # 字符画的高


# 将256灰度映射到70个字符上，也就是RGB值转字符的函数：
def get_char(r, g, b, alpha=256):  # alpha透明度
   if alpha == 0:
       return ' '
   length = len(ascii_char)
   gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 计算灰度
   unit = (256.0 + 1) / length
   return ascii_char[int(gray / unit)]  # 不同的灰度对应着不同的字符
   # 通过灰度来区分色块


if __name__ == '__main__':

   imgDown('http://gchat.qpic.cn/gchatpic_new/1840094972/732096208-2454784810-44E904AFD9B0773E83AE1D494D64DD37/0?term=2&is_origin=1') # 图片所在位置
   im = Image.open('pictures\\img.png')
   im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
   txt = ""
   for i in range(HEIGHT):
       for j in range(WIDTH):
           txt += get_char(*im.getpixel((j, i))) # 获得相应的字符
       txt += '\n'
   print(txt)  # 打印出字符画
   # 将字符画 写入文件中
   with open("pictures\\output.txt", 'w') as f:
       f.write(txt)