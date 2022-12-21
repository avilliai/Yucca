import requests
tocken=''
def getCom():
    url = "https://v2.alapi.cn/api/comment/submit"

    payload = "token="+tocken+"&id=1413812846&type=playlist"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text