#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
#接口地址
url ="https://ltpapi.xfyun.cn/v1/ke"
#开放平台应用ID
x_appid = "5ef2bd3f"
#开放平台应用接口秘钥
api_key = "31de729d88f38ead95e2dc1dff2d8250"
#语言文本
TEXT="前两天新传研圈又炸了，为什么呢？因为女神出新书了，彭兰老师的新作品《新媒体用户研究：节点化、媒介化、赛博格化的人》已经上新，有新的成熟的受众研究这作品上新，对于学术研究当然是好事，可以体系化的思考当前媒介环境下用户的特征及其认知模式与行为路径。但是对于考研的同学却犯了难，其实大家根本不知道这本书讲的是什么。只是一味的跟风在思考“到底要不要买？”的问题。"


def main():
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf-8'))
    return


if __name__ == '__main__':
    main()
