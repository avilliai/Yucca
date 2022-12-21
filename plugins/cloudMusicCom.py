import requests
tocken='Imiewqr8fMpApy3kqEJh'
def getCom():
    import requests

    url = "https://v2.alapi.cn/api/comment"

    payload = "token="+tocken+"&id="
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
if __name__ == '__main__':
    getCom()