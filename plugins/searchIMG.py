# -*- coding: utf-8 -*-
import requests

# API URL
api_url = "https://saucenao.com/search.php"

# API密钥
api_key = "6ccf5333e9c875421ff0764e2ed0c0cde1e3a0c7"

# 要搜索的图像的文件名
image_file = "D:\Mirai\YirisVoiceGUI\PythonPlugins\pictures\\abaia@a6aEaea8a.jpg"

# 设置请求头
headers = {
    "User-Agent": "MyScript/1.0",
}

# 设置请求参数
data = {
    "api_key": api_key,
    "db": "999",  # 999表示搜索所有数据库
}

# 将图像文件作为请求正文发送
with open(image_file, "rb") as f:
    files = {
        "file": f,
    }
    response = requests.post(api_url, headers=headers, data=data, files=files)

# 打印响应
print(response.text)
