

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import flask
import os
from wechatpy.utils import check_signature
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message, create_reply
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
import config



app = flask.Flask(__name__)


@app.route("/wx", methods=['POST', 'GET'])
def weixin_handler():
    # 从config文件中获取
    token = os.getenv('WECHAT_TOKEN', config.WECHAT_TOKEN)
    encodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', config.WECHAT_ENCODING_AES_KEY)
    appId = os.getenv('WECHAT_APP_ID', config.WECHAT_APP_ID)

    # 从请求中获取
    signature = flask.request.args.get("signature")
    timestamp = flask.request.args.get("timestamp")
    nonce = flask.request.args.get("nonce")
    echostr = flask.request.args.get("echostr")
    # encrypt_type = flask.request.args.get("encrypt_type")
    msg_signature = flask.request.args.get("msg_signature")

    '''
    print('signature:', signature)
    print('timestamp: ', timestamp)
    print('nonce:', nonce)
    print('echo_str:', echostr)
    print('encrypt_type:', encrypt_type)
    print('msg_signature:', msg_signature)
    '''

    crypto = WeChatCrypto(token, encodingAESKey, appId)
    try:
        check_signature(token, signature, timestamp, nonce)  # 签名验证
    except InvalidSignatureException:
        flask.abort(403)  # 校验token失败，证明这条消息不是微信服务器发送过来的

    if flask.request.method == "GET":  # 如果时明文模式 直接返回echoster
        return echostr
    elif flask.request.method == "POST":  # 如果时加密模式 先对传入的数据解密
        try:
            msg = crypto.decrypt_message(
                flask.request.data,
                msg_signature,
                timestamp,
                nonce
            )
            print('Descypted message: \n%s' % msg)  # 输出数据内容
        except (InvalidSignatureException, InvalidAppIdException):
            flask.abort(404)
        msg = parse_message(msg)  # 解析xml
        if msg.type == 'text':
            res = get_robot_reply(msg.content)
            reply = TextReply(message=msg)
            reply.content = '%s' % (res)
        elif msg.type == "image":  # 图片回复
            reply = ImageReply(message=msg)
            reply.media_id = msg.media_id
        else:
            reply = TextReply(content="暂时不支持此种类型的回复哦～", message=msg)
        print('Enscypted message: \n%s' % reply)
        # 返回加密信息
        return crypto.encrypt_message(
            reply.render(),
            nonce,
            timestamp
        )
    

def get_robot_reply(question):
    '''
    函数功能：对于特定问题进行特定回复，对于非特定问题进行智能回复
    
    参数描述：
    question 聊天内容或问题

    返回值：str，回复内容
    '''

    if "你叫" in question:
        answer = "我是东青啊^_^"
    elif "小组编号" in question:
        answer = "我们是第9组呢"
    elif "小组成员" in question:
        answer = "我们小组有7个人：组长 袁海东青，组员有肖龙超、沈彬、李金楷、郭炳辰、王君豪、杨中凡"
    elif "最新军事新闻头条" in question:
        answer = "百度新闻"
    else:
        try:
            # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg': question}).encode()  # 接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")  # 创建请求对象
            answer = urllib.request.urlopen(req).read().decode()  # 调用接口（即向目标服务器发出HTTP请求，并获取服务器的响应数据）
        except Exception as e:
            answer = "AI机器人出现故障！（原因：%s）" % e
    if answer != "":
        return answer
    else:
        return "在AI前进的道路上还是会有各种各样想不到的事情会发生"



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="80")

    