# -*- coding: utf-8 -*-
def weatherQ(city):
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
