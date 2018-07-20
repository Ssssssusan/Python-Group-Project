#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
- File name: machine_translation.py
- Author: Zhuying, Xulinyuan
- Date: 06/26/2018
- Description:
- Function List:
  1. _init_:设置构造函数，初始化所有参数
  2. translate: 调用有道和百度翻译类
'''

import baidu as B
import youdao as Y

class Fanyi(object):
    # Description: 有道翻译类
    def __init__(self, rec_text, in_lang, out_lang):
        '''
        :description: 构造函数，初始化有道翻译所需参数
        :param str in_lang: 源语言
        :param str out_lang: 目标语言
        :param str rec_text: 待翻译的文本
        '''
        self.rec_text = rec_text
        self.in_lang = in_lang
        self.out_lang = out_lang

    def translate(self):
        '''
        :description: 构造函数，初始化有道翻译所需参数
        '''
        t2 = Y.Youdao(self.in_lang, self.out_lang)
		#创建有道翻译实体
        flag = t2.translate(self.rec_text)
        if (flag == 'None'):
		#设置判断条件
            t1=B.Baidu()
            return t1.baidu_translate(self.in_lang, self.out_lang, self.rec_text)
			#创建百度翻译实体
        else:
            return flag
