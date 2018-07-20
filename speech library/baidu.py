# coding: utf8
'''
- File name: baidu.py
- Author: Xu Linyuan, Zhu Ying
- Date: 06/26/2018
- Description: 实现调用百度翻译API进行语音识别后的内容翻译
- Function List:
  1. baidu_translate: 包含机器翻译输入、发送、返回和输出的整个过程
'''

import http.client  
import hashlib  
import json  
import urllib  
import random  

langlist_Baidu={
        'zh-CN':'zh',
        'en-US':'en',
        'ja-JP':'jp',
        'ko-KR':'kor',
        'fr-FR':'fra',
        'es-ES':'spa',
        'ru-RU':'ru',
        'de-DE':'de',
        'pt-PT':'pt',
        'pl-PL':'pl',
        'sv-SE':'swe',
        'ar-EG*':'ara',
        'nl-NL':'nl',
        'fi-FI':'fin',
        'da-DK':'dan'
 }
key_list=[]
value_list=[]
for key,value in langlist_Baidu.items():
    key_list.append(key)
    value_list.append(value)
    
class Baidu():
    #def __init__(self, in_Lang, out_Lang,content):
    def baidu_translate(self,in_Lang,out_Lang,content):
        '''
        :description: 调用百度翻译API
        :param str fromLang: 源语言
        :param str toLang: 目标语言
        :param str myurl: 百度翻译 API 的链接
        :param str appid: 百度翻译 API 用户ID
        :param str secretKey: 百度翻译 API 用户密钥
        :param str q: 输入
        :param str sign: 加密数据
        :param str myurl: 发送请求中包含的所有信息
        :param str dst: 翻译结果
        '''
        fromLang=''
        toLang=''
        if in_Lang in key_list:
            key_index=key_list.index(in_Lang)
            fromLang=value_list[key_index]
        if out_Lang in key_list:
            key_index=key_list.index(out_Lang)
            toLang=value_list[key_index]
            
		# 因为语音识别的语言对设定与机器翻译的不同，首先进行语言对转化
        appid = '20170622000059949'  
        secretKey = 'V66eNSmKkfDXAKl7YGZv'  
        httpClient = None  
        myurl = '/api/trans/vip/translate'  
        q = content  
        salt = random.randint(32768, 65536)  
		# 产生随机数 ,对用户密码进行加密
        sign = appid + q + str(salt) + secretKey  
		# 先对sign.str进行统一编码，否则报错：Unicode-objects must be encoded before hashing
        sign = hashlib.md5(sign.encode()).hexdigest()  
		# 根据用户请求的url参数，生成sign
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(  
                q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(  
                        salt) + '&sign=' + sign  
                
        try:  
                httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')  
                httpClient.request('GET', myurl)  
                # response是HTTPResponse对象  
                response = httpClient.getresponse()  
                jsonResponse = response.read().decode("utf-8")
				# 获得返回的结果，结果为json格式  
                js = json.loads(jsonResponse)  
				# 将json格式的结果转换字典结构  
                dst = str(js["trans_result"][0]["dst"])  
				# 取得翻译后的文本结果  
                return dst 
				# 返回最终结果 

        except Exception as e:  
                    e=e
				#报错，此处设定为暂不返回报错原因
        finally:  
            if httpClient:  
                httpClient.close()  

#a=Baidu()
#print (a.baidu_translate('zh-CN','en-US','看电影'))