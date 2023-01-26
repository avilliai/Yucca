# coding: utf8
import random
import urllib.request

def random_str(random_length=6):
    """
    生成随机字符串作为验证码
    :param random_length: 字符串长度,默认为6
    :return: 随机字符串
    """
    string = 'a'
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789@$#_%'
    length = len(chars) - 1
    # random = Random()
    # 设置循环每次取一个字符用来生成随机数
    for i in range(7):
        string +=  ((chars[random.randint(0, length)])+'a')
    return string



def dict_download_img(url):
    img_url = url
    api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    header = {"Authorization": "Bearer " + api_token} # 设置http header
    request = urllib.request.Request(img_url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        ranpath = random_str()
        if str(url).endswith('.gif') or str(url).endswith('.GIF'):
            img_name = ranpath + ".gif"
        else:
            img_name = ranpath+".png"
        filename = "pictures\\dictPic\\"+ img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return img_name
    except:
        return "failed"


if __name__ == '__main__':
    dict_download_img('https://tvax3.sinaimg.cn/large/ec43126fgy1gwjqtn8f6bj229c38wnpk.jpg')