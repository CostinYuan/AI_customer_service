

import urllib.request
import urllib.parse
import time

def getRobotReply(question):
    '''
    函数功能：对于特定问题进行特定回复，对于非特定问题进行智能回复

    参数描述：
    question 聊天内容或问题

    返回值：str，回复内容
    '''

    if "你好" in question:
        answer = "你好？"
    elif "你叫啥" in question:
        answer = "你叫啥？"
    elif "你多大" in question:
        answer = "你多大？"
    else:
        try:
            # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg': question}).encode()  # 接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")
            answer = urllib.request.urlopen(req).read().decode()  # 调用接口（向目标服务器发出HTTP请求，并获取服务器的
        except Exception as e:
            answer = "AI机器人出现故障（原因：%s）" % e

    return answer


if __name__ == "__main__":
    while True:
        question = input("\n有何贵干？\n")
        print(getRobotReply(question))
        time.sleep(0.1)
