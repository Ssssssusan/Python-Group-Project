#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
- File name: speech_recognition.py
- Author: Yangruoyao, Sushan
- Date: 06/26/2018
- Description: 实现从麦克风读入或直接传入音频文件的语音识别
- Function List:
Class Speech2Text: 语音识别类
  1. check_format: 判断外部输入音频文件格式，不符合则向用户提示请转换格式后重新输入
  2. choose_input: 判断是麦克风输入还是外部音频输入
  3. microphone_input: 麦克风输入
  4. houndify_recognize: 调用 Houndify API 功能进行语音识别
  5. stop_notice: 在使用必应api进行语音识别前，提示用户可能因输入中含不止一处停顿，导致识别不完整
  6. check_bing_lang: 判断源语言是否是 Microsoft Bing API 可识别的语言
  7. bing_recognize: 调用 Microsoft Bing API 功能进行语音识别
  8. recognize: 语音识别整体串联流程
Class RecognizeError: 语音识别的错误信息类
  1. show_error: 如果未能成功识别，则打印两个API的错误信息
'''
from os import path
# import speech_library_full as sl
import speech_recognition as sl

class Speech2Text(object):
    ''' Description: 语音识别类 '''
    def __init__(self, in_lang, out_lang, houndify_id, houndify_key, bing_key, status, audio_file):
        '''
        :description: 构造函数，初始化语音识别所需参数
        :param string in_lang: 源语言
        :param string out_lang: 目标语言
        :param string houndify_id: Houndify API 用户ID
        :param string houndify_key: Houndify API 用户密钥
        :param string bing_key: Microsoft Bing API 用户密钥
        :param string status: 用户选择麦克风输入还是外部音频输入
        :param string audio_file:
            - if status = "microphone"，从麦克风输入，audio_file = ""
            - if status = "audio_file"，从外部音频输入，audio_file = "外部输入的语音文件名称"
        '''
        
        self.in_lang = in_lang
        self.out_lang = out_lang
        self.houndify_id = houndify_id
        self.houndify_key = houndify_key
        self.bing_key = bing_key
        self.error_flag1 = 0
        self.error_flag2 = 0
        self.status = status
        self.audio_file = audio_file

    def check_format(self):
        '''
        :description:
        进行语音识别时，将把音频文件转换为 AudioFile 类对象，
        AudioFile 类仅支持PCM/LPCM格式的WAV文件、AIFF和AIFF-C格式文件、FLAC格式文件。
        判断外部输入音频文件是否输入上述格式，不符合则向用户提示请转换格式后重新输入。
        :return str format_notice:
            - format_notice = ""，格式支持，可正确读入
            - format_notice != ""，向用户提示输入音频格式不支持，请转换格式后重新输入。
        '''
        format_notice = ""
        if not self.audio_file.strip().endswith(".wav") and not self.audio_file.endswith(".flac") and not self.audio_file.endswith(".aiff"):
            format_notice = "We only support '.wav','.flac','.aiff' files. Please transform your input audio file into the correct format."
        return format_notice

    def choose_input(self,r):
        '''
        :description: 判断是麦克风输入还是外部音频输入，根据不同输入形式初始化将进行语音识别的音频文件
        :param Recognizer r: Recognizer类实例，调用噪音消除和麦克风音频读入函数
        '''
        # 如果是麦克风读入，则调用麦克风输入函数获取音频存储地址
        if self.status == "microphone":
            self.audio_file = self.microphone_input(r)
        # 如果是外部音频文件读入，则检查格式是否支持
        else:
            format_notice = self.check_format()
            if not format_notice:
                # 如果外部文件传入成功且格式符合要求 或 麦克风读入成功
                if self.audio_file:
                    # 用文件名称生成完整音频存储路径信息
                    self.audio_file = path.join(path.dirname(path.realpath(__file__)), self.audio_file)
        # 如果上述步骤失败，则保留audio_file属性为空字符串，在整体串联函数中进行判断
        self.audio_file = self.audio_file

    def microphone_input(self,r):
        '''
        :description: 麦克风输入
        :param Recognizer r: Recognizer类实例，调用噪音消除和麦克风音频读入函数
        :return str audio_file: 麦克风读入后，写入的音频文件名称
        '''
        audio_file = ""
        r = sl.Recognizer()
        with sl.Microphone() as source:
            # 第1秒用作噪音消除
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            # 麦克风音频读入
            try:
                audio = r.listen(source)
                # 将输入音频写入wav文件
                audio_file = "microphone-results.wav"
                with open(audio_file, "wb") as f:
                    f.write(audio.get_wav_data())
            except Exception as e:
                print(e)
        return audio_file


    def houndify_recognize(self,r,audio,rec_text):
        '''
        :description: 调用 Houndify API 功能进行语音识别
        :param Recognizer r: Recognizer类实例，调用语音识别类函数
        :param AudioData audio: AudioData类实例，可被Recognizer类函数调用的audio转换形式
        :param str rec_text: 语音识别结果
        :return str rec_text: 语音识别结果
        '''
        # 调用 Houndify API 的用户ID, KEY
        # HOUNDIFY_CLIENT_ID、HOUNDIFY_CLIENT_KEY 均为base64编码的字符串
        HOUNDIFY_CLIENT_ID = self.houndify_id
        HOUNDIFY_CLIENT_KEY = self.houndify_key
        print("Recognizing......\n")
        try:
            rec_text = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        # 无法识别
        except sl.UnknownValueError:
            self.error_flag1 = 1
        # 无法连接API
        except sl.RequestError as e:
            self.error_flag1 = 2
        # 如果未识别成功，则rec_text空字符串原样返回
        return rec_text

    def stop_notice(self):
        '''
        :description:
        必应语音识别api只识别语音从开始到第一个停顿之间的部分（便于加标点，能使机器翻译识别得更准确）。
        在使用必应api进行语音识别前，提示用户可能因输入中含不止一处停顿，导致识别不完整。
        请用户自行决定是否拆分成多个短句重新输入。
        '''
        stop_notice = "Note: Bing API recognizes audio which has only one stop. " \
                      "If it bothers, please split your audio input into several parts, each ends with only one stop.\nRecognizing.....\n"
        print(stop_notice)

    def check_bing_lang(self):
        '''
        :description: 判断源语言是否是 Microsoft Bing API 可识别的语言
        :return str lang_notice:
            - if lang_notice = ""，Microsoft Bing API可识别源语言，将进行此API的调用。
            - if lang_notice != ""，Microsoft Bing API不可识别源语言，不进行此API的调用，
            并向用户提示此错误信息。
        '''
        lang_notice = ""
        # 读取Microsoft Bing API支持的语言列表
        list = []
        with open("./bing_lang.txt",'r', encoding="utf-8") as f:
            for line in f:
                list.append(line.strip())
        f.close()
        if self.in_lang not in list:
            lang_notice = "Sorry, your input language is not supported."
        return lang_notice

    def bing_recognize(self,r,audio,rec_text):
        '''
        :description: 调用 Microsoft Bing API 功能进行语音识别
        :param Recognizer r: Recognizer类实例，调用语音识别类函数
        :param AudioData audio: AudioData类实例，可被Recognizer类函数调用的audio转换形式
        :param str rec_text: 语音识别结果
        :return str rec_text: 语音识别结果
        '''
        # 调用 Microsoft Bing API 的用户KEY
        # BING_KEY为base64编码的字符串
        BING_KEY = self.bing_key
        try:
            rec_text = str(r.recognize_bing(audio, key=BING_KEY, language=self.in_lang, show_all=False))
        # 无法识别
        except sl.UnknownValueError:
            self.error_flag2 = 1
        # 无法连接API
        except sl.RequestError as e:
            self.error_flag2 = 2
        # 如果未识别成功，则rec_text空字符串原样返回
        return rec_text

    def recognize(self):
        '''
        :description: 语音识别整体流程封装成一个函数，用作在类外对本类功能的调用，得到返回值：识别结果、源语言、目标语言
        :return string rec_text: 语音识别结果
        :return string self.in_lang: 源语言
        :return string self.out_lang: 目标语言
        '''
        # 将识别结果字符串定义为空，便于机器翻译判断是否继续流程
        # 初始化调用API错误提示标记
        rec_text = ""
        self.error_flag1 = 0
        self.error_flag2 = 0

        # 实例化 Recognizer 类
        r = sl.Recognizer()
        # 得到音频输入，并保存到属性audio_file中
        self.choose_input(r)
        # 如果文件读入失败，则直接终止运行
        if not self.audio_file.strip():
            return rec_text, self.in_lang, self.out_lang
        # 调用 Recognizer 类中的 record() 函数读取音频文件
        # AudioFile 类支持PCM/LPCM格式的WAV文件、AIFF和AIFF-C格式文件、FLAC格式文件。
        with sl.AudioFile(self.audio_file) as source:
            audio = r.record(source)

        # 源语言是英语，则调用 Houndify API 功能进行语音识别
        if self.in_lang == "en-US":
            rec_text = self.houndify_recognize(r, audio, rec_text)
        else:
            # 源语言非英语时，无法调用 Houndify API，自动记为 "API无法连接"型错误。
            self.error_flag1 = 2
        # 源语言不是英语，或 Houndify API 没有得到识别结果
        if not rec_text.strip():
            # 判断是否是 Microsoft Bing API 可识别的语言
            lang_notice = self.check_bing_lang()
            # 如果可识别，则调用 Microsoft Bing API 功能进行语音识别
            if not lang_notice.strip():
                # 识别前提示用户可能因输入中含不止一处停顿，导致识别不完整；请用户自行判断是否重新输入。
                self.stop_notice()
                rec_text = self.bing_recognize(r, audio, rec_text)
            # 如果不可识别，则提示用户您的输入语言我们不支持。
            else:
                print(lang_notice)

        # 实例化错误信息类
        e = RecognizeError()
        # 打印两个API的错误信息
        e.show_error(self.error_flag1,self.error_flag2)
        #self.error_notice()

        # 如果未识别成功，则返回一个空字符串，便于机器翻译模块判断并停止工作
        # 如果识别成功，则返回识别结果
        return rec_text, self.in_lang, self.out_lang

    def error_notice(self):
        '''
        :description:
            语音识别不成功时，打印两个API的错误信息：
            - 只要有一个api正确识别，则不报错；
            - 两个都无法正确识别，且至少有一个为 "无法识别" 型错误，则向用户提示 "无法识别" 型错误；
            - 两个都无法正确识别，且都为 "API无法连接" 型错误，则向用户提示 "API无法连接" 型错误。
        '''
        error_note1 = "Sorry, our Speech Recognition service could not understand. Please speak again."
        error_note2 = "Sorry, we could not request results from Speech Recognition service."
        # 两个 API 都无法正确识别，才会输出错误提示信息
        if self.error_flag1 != 0 and self.error_flag2 != 0:
            # 两个都无法正确识别，且有一个为 "无法识别" 型错误
            if self.error_flag1 != self.error_flag2:
                print(error_note1)
            else:
                # 两个都无法正确识别，且都为 "无法识别" 型错误
                if self.error_flag1 == 1:
                    print(error_note1)
                # 两个都无法正确识别，且都为 "API无法连接" 型错误
                else:
                    print(error_note2)


class RecognizeError(object):
    ''' Description: 语音识别的错误信息类 '''

    def __init__(self):
        '''
        :description: 构造函数，初始化语音识别的两类错误状态和提示
        '''
        self.err_state0 = 0
        self.err_state1 = 1
        self.err_state2 = 2
        self.error1 = "Sorry, our Speech Recognition service could not understand. Please speak again."
        self.error2 = "Sorry, we could not request results from Speech Recognition service."

    def show_error(self, err1, err2):
        '''
        :description:
            语音识别不成功时，打印两个API的错误信息：
            - 只要有一个api正确识别，则不报错；
            - 两个都无法正确识别，且至少有一个为 "无法识别" 型错误，则向用户提示 "无法识别" 型错误；
            - 两个都无法正确识别，且都为 "API无法连接" 型错误，则向用户提示 "API无法连接" 型错误。
        '''
        # 两个 API 都无法正确识别，才会输出错误提示信息
        if err1 != self.err_state0 and err2 != self.err_state0:
            # 两个都无法正确识别，且有一个为 "无法识别" 型错误
            if err1 != err2:
                print(self.error1)
            else:
                # 两个都无法正确识别，且都为 "无法识别" 型错误
                if err1 == self.err_state1:
                    print(self.error1)
                # 两个都无法正确识别，且都为 "API无法连接" 型错误
                else:
                    print(self.error2)