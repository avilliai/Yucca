def write(title, content):
    global nid

    import requests
    import json

    url = "http://if.caiyunai.com/v1/dream/"

    # WARNING, this should be replaced by your token
    token =''  # your token

    # �������£�����Ѿ���������ʹ��֮ǰ������id

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

    # ѡ��ģ��

    # С��0�ţ�60094a2a9661080dc490f75a
    # С��1�ţ�601ac4c9bd931db756e22da6
    # ������601f92f60c9aaf5f28a6f908
    # ���飺601f936f0c9aaf5f28a6f90a
    # ���ã�60211134902769d45689bf75

    # �����ڱ��������ѡ��С��0�š�
    mid = "60094a2a9661080dc490f75a"

    # ������д

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

    # �ȴ����
    import time

    while True:

        time.sleep(1)

        # ��ȡ���
        payload = {
            "xid": xid,
            "nid": nid
        }

        response = requests.request("POST", url + token + "/novel_dream_loop", data=json.dumps(payload))

        if json.loads(response.text)['data']['count'] == 0:
            res = json.loads(response.text)['data']['rows']
            break

    return res


write("�����ս", "�������Ͻ���")