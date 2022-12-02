def write(title, content):
    global nid

    import requests
    import json

    url = "http://if.caiyunai.com/v1/dream/"

    # WARNING, this should be replaced by your token
    token =''  # your token

    # 创建文章，如果已经创建过就使用之前的文章id

    try:

        payload = {
            "content": content,
            "title": title,
            "nid": nid,
        }

    except:

        payload = {
            "content": content,
            "title": title,
        }

        response = requests.request("POST", url + token + "/novel_save", data=json.dumps(payload))

        nid = json.loads(response.text)['data']['nid']

    # 选择模型

    # 小梦0号：60094a2a9661080dc490f75a
    # 小梦1号：601ac4c9bd931db756e22da6
    # 纯爱：601f92f60c9aaf5f28a6f908
    # 言情：601f936f0c9aaf5f28a6f90a
    # 玄幻：60211134902769d45689bf75

    # 我们在本文例子里，选“小梦0号“
    mid = "60094a2a9661080dc490f75a"

    # 发起续写

    payload = {
        "content": content,
        "title": title,
        "mid": mid,
        "nid": nid
    }

    response = requests.request("POST", url + token + "/novel_ai", data=json.dumps(payload))

    try:
        xid = json.loads(response.text)['data']['xid']
    except:
        print(response.text)
        return;

    # 等待结果
    import time

    while True:

        time.sleep(1)

        # 获取结果
        payload = {
            "xid": xid,
            "nid": nid
        }

        response = requests.request("POST", url + token + "/novel_dream_loop", data=json.dumps(payload))

        if json.loads(response.text)['data']['count'] == 0:
            res = json.loads(response.text)['data']['rows']
            break

    return res


write("星球大战", "地球联合舰队")