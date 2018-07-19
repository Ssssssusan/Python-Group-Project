# Python-Group-Project

小组成员：苏珊、杨若瑶、朱莹、徐林源
项目主题：多语种自动语音翻译系统开发 —— 语音识别模块、机器翻译模块

项目文件列表：
    项目管理文件：
    Python Group Project.pptx -- 期末汇报展示
    Python小组项目说明_201807.docx -- 项目说明
    gantt-chart_Python.xlsx -- 分工与进度
    to-do-list_Python.xlsx -- 时间与任务管理
 
    程序代码文件：
    __main__.py -- 参数设置、测试代码
    sr_mt_ss.py -- 三个模块封装成一大类
    speech_recognize.py -- 语音识别模块封装成类
    machine_translation.py -- 机器翻译模块封装成类
    speech_synthesis.py -- 语音合成模块封装成类（假）
    bing_lang.txt -- bing语音识别支持语言
    youdao.py -- 有道机器翻译封装 
    baidu.py -- 百度机器翻译封装

    测试文件：
    test文件夹内，名称标记测试音频特征

注意：
    程序运行环境需求：需安装语音识别工具包、麦克风工具包
    在cmd中运行如下两行代码：
    pip install SpeechRecognition
    pip install pyaudio
