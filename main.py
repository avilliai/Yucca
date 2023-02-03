# -*- coding:utf-8 -*-
import json
config={"botName":" 填写机器人的名字","botQQ":" 填写机器人的QQ","master":" 填写你的QQ"}
with open('config.json','w',encoding='utf-8') as fp:
    configa=json.dump(config,fp,ensure_ascii=False)
