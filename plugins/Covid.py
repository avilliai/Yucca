import json

import requests

url1='https://api.vvhan.com/api/covid'
url2='https://api.vvhan.com/api/covid?city='


def getCovid(city):
    urk=url2+city
    covidStstus=requests.get(urk)

    result = open('Config\\covid.json', 'w')

    result.write(covidStstus.text)  # yang.text将yang这个json数据以字符形式使用
    result.close()  # 这里一定要关闭文件，不然写不进去
    open_json = open('Config\\covid.json', 'r', encoding='GBK')
    dict = json.load(open_json)  # json.load()将json转为python字典
    open_json.close()  # 到这里zd_json是一个`python字典`
    try:
        data=dict.get('data')

        times=data.get('updatetime')+'\n'

        status=data.get('now')
        newloc='新增确诊：'+str(status.get('sure_new_loc'))+'\n'
        newhid='新增无症状：'+str(status.get('sure_new_hid'))+'\n'
        present='现有确诊：'+str(status.get('sure_present'))+'\n'+'--------------------'+'\n'

        total=times+city+'\n'+newloc+newhid+present
        print(total)

        hisstatus = data.get('history')
        hiscnt = '累计确诊：'+str(hisstatus.get('sure_cnt')) + '\n'
        hiscure = '累计治愈：'+str(hisstatus.get('cure_cnt')) + '\n'
        hisdie = '累计死亡：'+str(hisstatus.get('die_cnt')) + '\n'
        histotal=hiscnt+hiscure+hisdie
        print(histotal)
        #返回疫情数据
        return total+histotal
    except:
        #没有对应城市数据
        print('数据未更新.....')
        return 1

if __name__ == '__main__':
    city='乌鲁木齐疫情'
    citys=city[0:-2]
    print(citys)