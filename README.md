# Danmu2Voice

实现弹幕转语音功能：
捕获bilibili直播间弹幕->交给API生成回复->使用另一款AI将回复转换为语音->播放

附带一个窗口(可隐藏)用来显示当前的对话。



使用python版本为3.10

## 安装

安装AI配音库[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)

请确保可以正常运行GPT-SoVITS的`webui.py` 和`api.py` 

运行`api.py` （注意修改路径）:

```sh
D:/0file/projs/GPT-SoVITS-v3lora-20250228/runtime/python.exe "D:/0file/projs/GPT-SoVITS-v3lora-20250228/api.py" -dr "D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/说话-既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。.wav" -dt "既然罗莎莉亚说足迹上有元素力，用元 素视野应该能很清楚地看到吧。" -dl "zh"
```

安装依赖

```sh
pip install -r requirements.txt
```

> 如果在安装bilibili-api的过程中遇到了“cython source“问题，可能是安装依赖pyyaml时遇到的问题，尝试下面的解决办法：
>
> https://stackoverflow.com/questions/77490435/attributeerror-cython-sources



