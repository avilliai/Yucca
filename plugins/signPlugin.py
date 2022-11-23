from cmath import e
from datetime import datetime
from functools import reduce
from mirai import GroupMessage
from sqlalchemy import false, true
from PIL import Image,ImageDraw,ImageFont
import os
import urllib.request, io
from mirai.models import Image as mImage
img = Image.open(r'PythonPlugins\plugins\Config\111.jpg')
temp=[]
temp2=[]
listAll=[]
def readTXT():
    with open(r'PythonPlugins\plugins\Config\\qiandaoInfo.txt','r',encoding='utf-8') as file:
        temp = str(file.read()).split('#')
        for i in temp:
            temp2=i.split("$")
            listAll.append(temp2)
def writeTXT():
    count=1
    count2=1
    l =listAll.__len__()
    with open(r'PythonPlugins\plugins\Config\\qiandaoInfo.txt','w',encoding='utf-8') as file:
        file.truncate(0)
        for i in listAll:
            for j in i:
                if count<4:
                    file.write(str(j)+"$")
                else:
                    if count2<l:
                        file.write(str(j)+"#")
                    else:
                        file.write(str(j))
                count+=1
            count=1
            count2+=1
        count2=1
readTXT()

def toint(s):
     return reduce(lambda x,y:x*10+y, map(lambda s:{'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}[s], s))

def makeImg(qq,group,time,n):
    URL = 'http://qlogo.store.qq.com/qzone/'+qq+'/'+qq+'/100'
    with urllib.request.urlopen(URL) as url:
        f = io.BytesIO(url.read())
    ico = Image.open(f).convert('RGBA')
    img_cp = img.copy()
    position = ((30),(105))
    img_cp.paste(ico,position,ico)
    font=ImageFont.truetype('simfang.ttf',20)
    ImageDraw.Draw(img_cp).text((200,110),"签到成功！\n已经连续签到第"+n+"天！\n\nqq："+qq+"\n群号："+group+"\n签到时间："+time,(0,0,0),font=font)
    rgb_img = img_cp.convert('RGB')
    rgb_img.save(r'C:\Users\Administrator\Desktop\moyao\plugins\pyPlugins\config\tempimg.jpg')

def main(bot):
    @bot.on(GroupMessage)
    async def start(event:GroupMessage):
        if str(event.message_chain)=="签到":
            group = str(event.group.id)
            qq = str(event.sender.id)
            time = int(datetime.now().strftime('%Y%m%d'))
            flage = false
            nbINFO=[]
            n=0
            for i in range(0,listAll.__len__()):
                if listAll[i][1]==qq:
                    for num in listAll[i]:
                        nbINFO.append(num)
                    flage=true
                    n=i
            if flage==false:
                nbINFO=[group,qq,1,time]
                makeImg(qq,group,str(time),"1")
                await bot.send(event,[
                    mImage(path='C:/Users/Administrator/Desktop/moyao/plugins/pyPlugins/config/tempimg.jpg')
                ])
                os.remove(r'C:\Users\Administrator\Desktop\moyao\plugins\pyPlugins\config\tempimg.jpg')
                listAll.append(nbINFO)
                writeTXT()
            else :
                ltime=0
                try:
                    ltime = toint(nbINFO[3])
                except TypeError:
                    ltime = nbINFO[3]
                if time - ltime == 1:
                    nbINFO[2] = str(toint(nbINFO[2])+1)
                    nbINFO[3]=str(time)
                    nbINFO[0]=group
                    listAll.pop(n)
                    makeImg(qq,group,str(time),str(nbINFO[2]))
                    await bot.send(event,[
                        mImage(path='C:/Users/Administrator/Desktop/moyao/plugins/pyPlugins/config/tempimg.jpg')
                    ])
                    os.remove(r'C:\Users\Administrator\Desktop\moyao\plugins\pyPlugins\config\tempimg.jpg')
                    listAll.append(nbINFO)
                    writeTXT()
                elif time - ltime > 1:
                    nbINFO[2]=1
                    nbINFO[3]=str(time)
                    nbINFO[0]=group
                    listAll.pop(n)
                    makeImg(qq,group,str(time),"1")
                    await bot.send(event,[
                        mImage(path='C:/Users/Administrator/Desktop/moyao/plugins/pyPlugins/config/tempimg.jpg')
                    ])
                    os.remove(r'C:\Users\Administrator\Desktop\moyao\plugins\pyPlugins\config\tempimg.jpg')
                    listAll.append(nbINFO)
                    writeTXT()
                elif time - ltime == 0:
                    if group==nbINFO[0]:
                        await bot.send(event,"你今天已经在本群签过到了！")
                    elif group!=nbINFO[0]:
                        await bot.send(event,"你今天已经在其他群签过到了！")


