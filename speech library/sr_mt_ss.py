#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
- File name: sr_mt_ss.py
- Author: Sushan
- Date: 06/26/2018
- Description: 整合语音识别、机器翻译、语音合成（假）三个模块形成一类
- Function List:
  1. microph: 实现从麦克风获取声音语音识别、机器翻译、并进行语音生成，输出全部中间结果，并可从外部获取三个结果
  2. audiofile: 实现从麦克风获取声音语音识别、机器翻译、并进行语音生成，输出全部中间结果，并可从外部获取三个结果
'''

import speech_recognize as sp
import machine_translation as mt
import speech_synthesis as ss


class Speech2Speech(object):
    ''' 三类整合 '''
    def __init__(self, in_lang, out_lang, houndify_id, houndify_key, bing_key):
        '''
        :description: 构造函数，初始化所需参数
        :param string in_lang: 源语言
        :param string out_lang: 目标语言
        :param string houndify_id: Houndify API 用户ID
        :param string houndify_key: Houndify API 用户密钥
        :param string bing_key: Microsoft Bing API 用户密钥
        '''

        self.in_lang = in_lang
        self.out_lang = out_lang
        self.houndify_id = houndify_id
        self.houndify_key = houndify_key
        self.bing_key = bing_key

    def microph(self):
        '''
        :description:
        用麦克风输入语音调用该函数
        分别实例化三个模块的类，并依次调用函数，完成从语音-文字-翻译-语音的流程
        :return str rec_text: 语音识别结果
        :return str mt_text: 机器翻译结果
        :return str au_path: 语音结果
        '''
        # 初始化机器翻译和语音合成结果，便于调用时作是否成功的判断
        mt_text = ""
        au_path = ""
        # 用户选择麦克风输入
        audio_file = ""
        status = "microphone"
        # 创建语音识别类的实例，调用语音识别函数
        t = sp.Speech2Text(self.in_lang, self.out_lang, self.houndify_id, self.houndify_key, self.bing_key, status, audio_file)
        rec_text, in_lang1, out_lang1 = t.recognize()
        # 如果语音识别成功（如不成功则在语音识别模块中报错，不运行机器翻译和语音合成模块直接返回。）
        if rec_text.strip():
            print("——————————语音识别结果——————————")
            print("You said: " + rec_text)
            print("input language: " + in_lang1)
            print("output language: " + out_lang1)

            # 创建机器翻译类的实例，调用机器翻译函数
            t2 = mt.Fanyi(rec_text, self.in_lang, self.out_lang)
            mt_text = t2.translate()
            print("——————————机器翻译结果——————————")
            print("You said: " + mt_text)

            # 创建语音合成类的实例，调用语音合成函数
            t3 = ss.Text2Speech(mt_text, self.out_lang)
            au_path, au_lang = t3.synthesis()
            print("——————————语音合成结果——————————")
            print("Audio Path: " + au_path)
            print("Audio language: " + au_lang)

        return rec_text, mt_text, au_path

    def audiofile(self, audio_file):
        '''
        :description:
        用音频文件输入语音调用该函数
        分别实例化三个模块的类，并依次调用函数，完成从语音-文字-翻译-语音的流程
        :return str rec_text: 语音识别结果
        :return str mt_text: 机器翻译结果
        :return str au_path: 语音结果
        '''
        # 初始化机器翻译和语音合成结果，便于调用时作是否成功的判断
        mt_text = ""
        au_path = ""
        # 用户选择外部音频输入，获取音频文件名称
        status = "audio_file"
        # 创建语音识别类的实例，调用语音识别函数
        t = sp.Speech2Text(self.in_lang, self.out_lang, self.houndify_id, self.houndify_key, self.bing_key, status, audio_file)
        rec_text, in_lang1, out_lang1 = t.recognize()
        # 如果语音识别成功（如不成功则在语音识别模块中报错，不运行机器翻译和语音合成模块直接返回。）
        if rec_text.strip():
            print("——————————语音识别结果——————————")
            print("You said: " + rec_text)
            print("input language: " + in_lang1)
            print("output language: " + out_lang1)

            # 创建机器翻译类的实例，调用机器翻译函数
            t2 = mt.Fanyi(rec_text, self.in_lang, self.out_lang)
            mt_text = t2.translate()
            print("——————————机器翻译结果——————————")
            print("You said: " + mt_text)

            # 创建语音合成类的实例，调用语音合成函数
            t3 = ss.Text2Speech(mt_text, self.out_lang)
            au_path, au_lang = t3.synthesis()
            print("——————————语音合成结果——————————")
            print("Audio Path: " + au_path)
            print("Audio language: " + au_lang)

        return rec_text, mt_text, au_path

