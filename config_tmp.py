#================
# AI 配音
# wavs和voice_prompt_texts的顺序要一一对应
wavs = ["D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/平静-好耶！《特尔克西的奇幻历险》出发咯！.wav",
        "D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/生气-呜哇好生气啊！不要把我跟一斗相提并论！.wav",
        "D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/说话-既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。.wav",
        "D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/疑问-哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？.wav"]
voice_prompt_texts = ["好耶！《特尔克西的奇幻历险》出发咯！",
                "呜哇好生气啊！不要把我跟一斗相提并论！",
                "既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。",
                "哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？"]

# 默认语音服务器地址
voice_host_url = "http://127.0.0.1:9880"

#================ 
# LLM API 大语言模型设置
# API的提示词
LLM_AI_system_prompt = "You are a helpful assistant."
prompt_path = "prompt.txt"

# 请务必设置自己的API Key
LLM_API_url = "https://api.siliconflow.cn/v1/chat/completions"
LLM_Authorization = "Bearer sk-zckdxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxoinep"
#================ 
# bilibili live
# 直播间房间号
ROOMID = 1732028631
# 你自己的账号的uid
UID = 381771544
# cookies
credential_sessdata = "2860b4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxEC"
credential_bili_jct = "f1fxxxxxxxxxxxxxxxxxxxxxxxxxxfcc"
#================
# log日志
history_path = "./logs/history.log"
log_path = "./logs/log.log"
## log的日志等级和日志格式在mylog.py中设置