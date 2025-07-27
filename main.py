import requests
from pydub import AudioSegment
import simpleaudio as sa
import io
import threading
import json

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mywindow as Window
import config
from mylog import logger
import write2txt

with open(config.prompt_path,encoding='utf-8') as f:
    AI_prompt = f.read()
## 打开文字转语音功能
import subprocess

import socket
import time

def wait_for_port(port, host='127.0.0.1', timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                logger.info(f"端口 {port} 已开放！")
                return True
        except (ConnectionRefusedError, socket.timeout):
            if time.time() - start_time > timeout:
                logger.error(f"等待端口 {port} 超时", exc_info=True)  # 记录日志并包含堆栈
                raise TimeoutError(f"等待端口 {port} 超时")
            time.sleep(0.5)  # 避免CPU占用过高

#TODO 莫名奇妙的bug
# 所以在代码中没有使用这个函数,选择了手动运行GPT-SoVITS-v3lora
import os
def start_play_audio():
    """
    启动AI配音模型
    """
    # 非阻塞启动
    working_dir = r"D:/0file/projs/GPT-SoVITS-v3lora-20250228/"
    python_path = os.path.join(working_dir,"runtime",'python.exe')
    script_path = os.path.join(working_dir, "api.py")   
    default_audio = os.path.join(working_dir,"voice","paiMeng","说话-既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。.wav")
    defalut_text = "既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。"
    language = "zh"
    # 调试输出
    print("最终Python路径:", os.path.abspath(os.path.join(working_dir, python_path)))
    print("最终Python路径:", os.path.abspath(os.path.join(working_dir, script_path)))
    process = subprocess.Popen(
        [python_path,script_path,
         "-dr" ,default_audio,
         "-dt",defalut_text,
         "-dl",language],
        stdout=subprocess.PIPE,  # 重定向输出
        stderr=subprocess.PIPE,
        text=True,
        cwd=working_dir
    )
    print("等待启动AI配音模型...")
    wait_for_port(9880)
    print("启动成功")


def playWav(content):
    """
    播放wav文件
    """
    def _play():
        try:
            audio = AudioSegment.from_wav(io.BytesIO(content))
            audio = audio - 15 # 降低声音大小
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True
            )
            stream.write(audio.raw_data)
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            logger.error(f"[播放错误] {e}")

    thread = threading.Thread(target=_play)
    thread.start()

import re
def remove_bracketed_content(text):
    """
    移除文本中的括号及其内部的内容,AI生成的文本中括号内的部分跳过不读。
    """
    # 使用正则表达式匹配括号及其内部的内容
    cleaned_text = re.sub(r'\([^)]*\)', '', text)
    cleaned_text = re.sub(r'（[^)]*）', '', cleaned_text)
    cleaned_text = re.sub(r'\[[^\]]*\]', '', cleaned_text)
    return cleaned_text
def choose_tone(text:str):
    """
    根据输入的文本选择合适的音调
    """
    if text.startswith("(平静)"): 
        tone = 0
    elif text.startswith("(生气)"): 
        tone = 1
    elif text.startswith("(说话)"): 
        tone = 2
    elif text.startswith("(疑问)"): 
        tone = 3
    else:
        tone = 2
    text = remove_bracketed_content(text)
    return text,tone

def text2wav(text: str):
    """
    将文本转换为wav文件
    """
    text,tone = choose_tone(text)
    
    url = config.voice_host_url
    data = {
        "refer_wav_path": config.wavs[tone],
        "prompt_text": config.voice_prompt_texts[tone],
        "prompt_language": "zh",
        "text": text,
        "text_language": "zh",
        "cut_punc": "，。"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            playWav(response.content)
            logger.info("已提交播放任务，可继续输入...")
        else:
            logger.error(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        logger.error(f"[转换错误] {e}")

default_messages = [
    {"role": "system", "content": AI_prompt}
]
messages = []


def get_deepseek_response(content): 
    # messages 是一个列表，每一项是一个字典
    # 示例：messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
    url = config.LLM_API_url
    messages.append({"role": "user", "content": content})
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": default_messages + messages,
        "stream": False,
        "max_tokens": 512,
        "stop": None,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": [
            {
                "type": "function",
                "function": {
                    "description": "<string>",
                    "name": "<string>",
                    "parameters": {},
                    "strict": False
                }
            }
        ]
    }
    headers = {
        "Authorization": config.LLM_Authorization,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    json_response = json.loads(response.text)
    if json_response["choices"][0]["message"]["content"]:
        if(len(messages) > 20):
            messages.pop(0)
            messages.pop(0)
        messages.append({"role": "assistant", "content": json_response["choices"][0]["message"]["content"]})
        return json_response["choices"][0]["message"]["content"]
    messages.pop()
    return 


# 播放音频
import pyaudio
# 显示窗口
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint

app = QApplication([])
window = Window.DraggableWindow()

import threading
from bulletListener import DanmuListener
from queue import Queue

danmu_queue = Queue()
max_queue_size = 10
def handle_danmu(msg,uname,face_url):
    logger.info(f"[弹幕回调] {msg}")
    if msg[0] == '/' :
        return
    if(danmu_queue.qsize() >= max_queue_size):
        Window.change_window_text( "弹幕队列已满:"+msg) # 更新窗口文本
        return
    danmu_queue.put(msg,timeout=1.0)
    while(danmu_queue.qsize() > 0):
        danmu_AI_TTS(uname,danmu_queue.get())
    
lock = 0 # 锁住函数danmu_AI_TTS

def danmu_AI_TTS(uname,msg):
    global lock
    while(lock == 1): # 锁住
        continue
    lock = 1
    Window.change_window_text(window, uname+":"+msg) # 更新窗口文本
    content = get_deepseek_response(msg) # 获取deepseek返回的结果
    logger.info(f"[AI回调] {content}")
    Window.change_window_text(window, uname+":"+msg+"\nAI:"+content) # 更新窗口文本
    write2txt.write_append(uname+":"+msg+"\nAI:"+content+"\n",config.history_path)
    text2wav(content) # AI配音
    lock = 0
# 初始化

# 创建监听器
listener = DanmuListener(config.ROOMID, callback=handle_danmu)

# 启动监听线程
def run_listener():
    listener.start()


def main():
    # start_play_audio()
    window.resize(600, 400)
    
    window.show()
    thread = threading.Thread(target=run_listener)
    thread.daemon = True  # 设为守护线程，主程序退出时自动结束
    thread.start()
    print("输入文本进行转换（输入 exit 退出）")
    logger.info("[文本转换] 开始(输入exit退出)")
    while True:
        try:
            text = input("\n请输入要转换的文本：")
            if text.lower() == 'exit':
                logger.info("[文本转换] 结束")
                break
            Window.change_window_text(window, "\nAI:"+text) # 更新窗口文本
            text2wav(text)
        except KeyboardInterrupt:
            logger.info("[文本转换] 用户主动退出")
            break
        except Exception as e:
            logger.error("[文本转换] 错误")


if __name__ == "__main__":
    main()