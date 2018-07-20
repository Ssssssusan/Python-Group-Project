#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
- File name: __main__.py
- Author: Sushan
- Date: 06/26/2018
- Description: 联通语音识别、机器翻译、语音合成（假）三个模块
- Notice: 运行程序前需在cmd中用“pip install SpeechRecognition”指令安装 SpeechRecognition Library 库
'''

import sr_mt_ss as wh

# 源语言与目标语言选择
# in_lang = "xx-XX"
in_lang = "zh-CN"
#in_lang = "en-US"
#in_lang = "fr-FR"
#out_lang = "en-US"
#out_lang = "zh-CN"
out_lang = "fr-FR"

# 配置api的id和key
# houndify:
houndify_id = "qH3QmCL_aHwLhvSqBRYhkQ=="
houndify_key = "wy5jD_Bb3fyXWL3sUl60iTePh_AqjXEWQEwyARB_Tslemz53E9OWDZzB2VPG27qgOnBezlfpXelQH1lASNwl0g=="
# bing:
# bing_key = "759fe37038e4797b541d908eaa3f419"  # 备用key，两个key均仅可应用7天
bing_key = "e9938f010a354d28a74d4e3ef56c653e"

# 实例化整合类
t = wh.Speech2Speech(in_lang, out_lang, houndify_id, houndify_key, bing_key)

# 用音频文件输入语音调用该函数
# 外部音频输入可选测试文件："ch-long-stop.wav" /"ch-long-non-stop.wav" /"ch-short.wav" /"en-long-stop.wav" /"en-long-non-stop.wav" /"en-short.wav" / "fr_Le Papillon_part.wav"
# audio_file = "./test/zh.wav"
# audio_file = "./test/zh.flac"
# audio_file = "./test/zh.aiff"
audio_file = "./test/ch-long-stop.wav"
rec_text, mt_text, au_path = t.audiofile(audio_file)

# 用麦克风输入语音调用该函数
#rec_text, mt_text, au_path = t.microph()


#可从外部获取三个模块的结果
if rec_text.strip():
    print("语音识别结果: "+rec_text)
if mt_text.strip():
    print("机器翻译结果: "+mt_text)
if au_path.strip():
    print("语音合成结果: "+au_path)





