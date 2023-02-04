# -*- coding: gbk -*-
import json

import requests
tocken='Imi8fMpApy3kqEJh'
def getCom():

    url = "https://v2.alapi.cn/api/comment"

    payload = "token="+tocken+"&id="
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    a=response.json()
    #dia=json.loads(response)
    #re=dia.get("comment_content")
    #print(response.json())
    data=a.get("data")
    da=data.get('comment_content')+'\n          ---《'+data.get("title")+'》\n              '+ data.get('published_date')
    #print(da)
    return da
if __name__ == '__main__':
    getCom()