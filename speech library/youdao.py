#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
- File name: youdao.py
- Author: Zhuying, Xulinyuan
- Date: 06/26/2018
- Description: 实现调用有道翻译API进行语音识别后的内容翻译
- Function List:
  1. _init_:构造函数接收源语言和目标语言并初始化其他参数
  2.getUrlEncodedData: 将数据进行编码请求有道 API 返回编码后的数据
  3. parseHtml: 解析内容并返回结果
  4. translate: 调用getUrlEncodedData和 parseHtml函数
'''

import urllib.request
import json
import time
import hashlib

langlist_Youdao={
        'zh-CN':'zh-CHS',
        'en-US':'EN',
        'ja-JP':'ja',
        'ko-KR':'ko',
        'fr-FR':'fr',
        'es-ES':'es',
        'ru-RU':'ru',
        'de-DE':'de',
        'pt-PT':'pt',
        'pl-PL':'pl',
        'sv-SE':'sv',
        'ar-EG*':'ar',
        'nl-NL':'nl',
        'nb-NO':'no',
        'fi-FI':'fi',
        'da-DK':'da'
        }
key_list=[]
value_list=[]
for key,value in langlist_Youdao.items():
    key_list.append(key)
    value_list.append(value)
    
class Youdao():
    ''' Description: 有道翻译类 '''
    def __init__(self,in_Lang,out_Lang):
        '''
        :description: 构造函数，初始化有道翻译所需参数
        :param str langFrom: 源语言
        :param str langTo: 目标语言
        :param str url: 有道翻译 api 的链接
        :param str appKey: 有道翻译 API 用户ID
        :param str appSecret: 有道翻译 API 用户密钥
        '''
        if in_Lang in key_list:
            key_index=key_list.index(in_Lang)
            langFrom=value_list[key_index]
        if out_Lang in key_list:
            key_index=key_list.index(out_Lang)
            langTo=value_list[key_index]
            
        self.url = 'https://openapi.youdao.com/api/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",}
        self.appKey = '08d00a94ef3ac62f'
        self.appSecret = 'oRqukWQZni4iof6X0uhfHj9z0pXponZa'
        self.langFrom = langFrom   # 翻译前文字语言,auto为自动检查
        self.langTo = langTo     # 翻译后文字语言,auto为自动检查

    def getUrlEncodedData(self, queryText):
        '''
        :description:将数据进行url编码，并返回编码后的数据
        :param str queryText: 待翻译的文字
        :param str salt: 加密值
        :param str sign: 发送请求的所有数据
        :return str data: 返回url编码后的数据
        '''
        salt = str(int(round(time.time() * 1000))) 
        # 产生随机数 ,对用户密码进行加密
        sign_str = self.appKey + queryText + salt + self.appSecret
        # 先对sign.str进行统一编码，否则报错：Unicode-objects must be encoded before hashing
        sign = hashlib.md5(sign_str.encode("utf8")).hexdigest()  
        # 根据用户请求的url参数，生成sign签名
        payload = {
            'q': queryText,
            'from': self.langFrom,
            'to': self.langTo,
            'appKey': self.appKey,
            'salt': salt,
            'sign': sign
        }
        data = urllib.parse.urlencode(payload)
        return (data)
        #返回编码后的数据
    def parseHtml(self, html):
        '''
        description: 解析页面，输出翻译结果
        :param str html: 翻译返回的页面内容
        :return str translationResult: 返回翻译结果
        '''
        data = json.loads(html.decode('utf-8'))
        #解析页面，返回结果
        translationResult = data['translation']
        #将结果赋给translationReasult
        if isinstance(translationResult, list):
            translationResult = translationResult[0]
        return translationResult                   
        # 返回调用api的翻译结果
        
    def translate(self, queryText):
        '''
        description: 将 getUrlEncodedData 和 parseHtml 串起来
        :return str self.parseHtml: 返回翻译结果
        '''
        data = self.getUrlEncodedData(queryText)  
        # 获取url编码过的数据
        target_url = self.url + '?' + data    
        # 构造目标url
        request = urllib.request.Request(target_url, headers=self.headers)  
        # 构造请求
        response = urllib.request.urlopen(request)  
        # 发送请求
        return self.parseHtml(response.read())    
        # 解析并显示翻译结果


