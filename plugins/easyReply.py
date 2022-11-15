
import random
import sys

import json



def addReplys(ass):
    message=ass[2:]
    messageS=message.split('#')
    #读取字典
    file = open('Config\\dict.txt', 'r')
    js = file.read()
    dict = json.loads(js)
    print('已读取字典')
    #print(dict)
    #print('---------')
    file.close()

    #对传入的字符串进行处理并加入字典
    #如果已经有关键字
    if (messageS[0] in dict):
        replyValue=dict.get(messageS[0])
        replyValue.append(messageS[1])
        print('已有关键字，追加')
        #print(replyValue)
    #没有关键字则创建
    else:
        dict[messageS[0]] = [messageS[1],]
        print(dict)
    #重新写入
    print(dict)
    js = json.dumps(dict)
    file = open('Config\\dict.txt', 'w')
    file.write(js)
    file.close()
    return '添加完成'



#dict[messageS[0]]=messageS[1]
#print(dict)


def dels(messagess):
    file = open('plugins\\Config\\dict.txt', 'w')
    js = file.read()
    dict = json.loads(js)
    messageS=messagess[2:]
    if (messageS in dict):
        dict.pop(messageS)
        js = json.dumps(dict)
        file = open('plugins\\Config\\dict.txt', 'w')
        file.write(js)
        file.close()
        return '已删除'
    else:
        return '似乎没有对应的关键词'
'''def main(bot):
    @bot.on(Startup)
    async def avillia(event: Startup):
        while True:
            avillia

    @bot.on(GroupMessage)
    async def avillia(event: GroupMessage):
        replyMes = reply(str(event.message_chain))
        if replyMes != 0:
            if len(replyMes) < 40:
                ran = random.randint(0, 1)
                if ran == 0:
                    ranpath = random_str()
                    out = sys.argv[0][:-20] + 'PythonPlugins\\plugins\\voices\\' + ranpath + '.wav'
                    tex = '[JA]' + translate(replyMes) + '[JA]'
                    voiceGenerate(tex, out)
                    await bot.send(event, Voice(path=out))'''


#with open("config\\replyDic.txt",'a') as f:
if __name__ == '__main__':
    print('当前路径' + sys.argv[0])
    addReplys('avillia#1111111')


