# -*- coding: utf-8 -*-
import re

import openai
from PIL.ImageDraw import ImageDraw
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# Set the API key for the openai module
openai.api_key = "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"
def GPT(stra,mode=1):
    # Use the GPT-3 model to generate text
    print('已接受问题'+stra)
    prompt = stra
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=540,
        n=1,
        temperature=0.5,
    )

    # Print the generated text

    str0 = str(response["choices"][0]["text"])
    str0=str0.replace('\n\n','\n')
    if mode==0:
        print(str0)
        return str0
    else:
        s = re.sub(r"(.{45})", "\\1\r\n", str0)
        print(s)
        if len(s)>1500:
            sr1=s[0:1200]
            sr2 = s[1200:]
            imageFile = "Config\\back.png"
            tp = Image.open(imageFile)

            font = ImageFont.truetype('Config/SiYuanHeiTiJiuZiXing-Regular-2.ttf', 47)
            draw = ImageDraw.Draw(tp)
            draw.text((65, 63), sr1, (12, 0, 6), font=font)
            draw.text((1269, 437), sr2, (12, 0, 6), font=font)
            # 在图片上添加文字 1

            # 保存
            tp.save("pictures\\reply.png")
            return 'pictures\\reply.png'

        else:
            #print('即将返回'+str1)

            # 打开底版图片
            imageFile = "Config\\back.png"
            tp = Image.open(imageFile)

            font = ImageFont.truetype('Config/SiYuanHeiTiJiuZiXing-Regular-2.ttf', 47)
            draw = ImageDraw.Draw(tp)
            draw.text((65, 63), s, (12, 0, 6), font=font)
            # 在图片上添加文字 1

            # 保存
            tp.save("pictures\\reply.png")

            return 'pictures\\reply.png'



if __name__ == '__main__':
    GPT('请为我总结Alan Watts的哲学理念，尽可能全面，用中文回复')
