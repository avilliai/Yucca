import json
import os
import urllib

import requests

from plugins.RandomStr.RandomStr import random_str

#url = 'https://iw233.cn/api.php?sort=random' # 接口地址
from plugins.imgDownload import download_img

url='http://api.kurlsq.cn/API/acgtp/api.php?type=json'
headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
def pic():

    r = requests.get(url, headers=headers).json()
    #print(type(r))
    url1=r.get('img')
    print(url1)
    img_url = url1
    api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    dicta=[]
    if url1 not in dicta:
        dicta.append(url1)
    else:
        pic()

    header = {"Authorization": "Bearer " + api_token}  # 设置http header
    request = urllib.request.Request(img_url, headers=header)
    try:
        response = urllib.request.urlopen(request)

        ranpath = random_str()
        img_name = ranpath+".png"
        filename = "pictures/" + img_name
        #print(filename)
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read())  # 将内容写入图片
            return filename
    except:
        return "failed"


    '''while True:
        ranpath = random_str()
        exist = os.path.isfile("pictures\\" + ranpath + ".jpg")
        direxist =os.path.isdir("pictures")
        if direxist:
            if exist:
                continue
            else:
                break
        else:
            os.mkdir("pictures")
            continue

    with open("pictures\\" + ranpath + ".jpg", mode="wb") as f:
        f.write(r.content)  # 图片内容写入文件
    return "pictures\\" + ranpath + ".jpg"'''
if __name__ == '__main__':
    '''s=input("输入1开始执行")
    i=0
    if s=="1":
        while i<=10:
            pic()
            i+=1'''
    pic()

