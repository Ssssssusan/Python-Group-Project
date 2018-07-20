#!/usr/bin/env python
# -*- coding: utf-8 -*
"""语音合成模块（假）"""
from os import path
class Text2Speech(object):
    # 语音合成类
    def __init__(self, mt_text,out_lang):
        # @description：构造函数
        # @param string mt_text -- 机器翻译结果
        # @param string out_lang -- 目标语言

        self.mt_text = mt_text
        self.out_lang = out_lang

    def synthesis(self):
        # @description：语音合成
        # @return string audio_file -- 语音合成结果，音频文件储存位置
        # @return string out_lang -- 音频文件语言
        audio_name = "synthesis_result.wav"
        audio_file = path.join(path.dirname(path.realpath(__file__)), audio_name)

        return audio_file, self.out_lang