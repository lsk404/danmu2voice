# windows安装Danmu2Voice

仓库链接 https://github.com/lsk404/danmu2voice 

点点star吧求求啦~

## 注意事项

本文使用环境如下：

- conda 24.9.2
- pip 25.1
- python 3.10.16(>=3.8)
- MSVC v143
- Windows 11 SDK 

## 安装GPT-SoVITS

[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 是一款开源的AI配音项目，方便部署。

官方安装教程戳这里：https://github.com/RVC-Boss/GPT-SoVITS?tab=readme-ov-file

1. 下载[整合包（附链接）](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/dkxgpiy9zb96hob4#KTvnO)

得到和`GPT-SoVITS-v3lora-20250228` 类似的压缩包，解压他。

2. 下载语音包

本文以派蒙模型为例，[bilibili 视频链接](https://www.bilibili.com/video/BV1Yu4m1N79m/)

我使用的模型-> [夸克网盘下载链接](https://pan.quark.cn/s/9da1ef8b9feb)

(将下载的内容存放到合适的地方,之后还要用到他们的path)

修改config.py中的参数(sovits_path对应xxx.pth , gpt_path对应xxx.ckpt)

```python
sovits_path = "D:/0file/projs/GPT-SoVITS-v3lora-20250228/SoVITS_weights/派蒙_e10_s19390.pth"
gpt_path = "D:/0file/projs/GPT-SoVITS-v3lora-20250228/GPT_weights/派蒙-e10.ckpt"
```

> 请确保可以正常运行GPT-SoVITS的`webui.py` 和`api.py` 

## 安装danmu2voice

1. 克隆本仓库

2. 安装依赖

```sh
pip install -r requirements.txt
```

> 如果在安装bilibili-api的过程中遇到了“cython source“问题，可能是安装依赖pyyaml时遇到的问题，尝试下面的解决办法：
>
> https://stackoverflow.com/questions/77490435/attributeerror-cython-sources.

## 获取大语言模型的API

自选一个大语言模型平台，充值获取API使用额度（或者使用赠送的免费额度）。

> 如果你还没有合适的LLM的API平台，那么可以使用我的邀请码yWv37GkL注册[硅基流动](https://cloud.siliconflow.cn/i/yWv37GkL)，可以获得额外的免费额度！

获取API_url和Authorization

下面以硅基流动的API调用过程举例：

- Authorization: 在API密钥界面新建一个API，密钥描述随便写。

之后会得到类似`sk-zckdxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxjoinep` 的字符串。（这是你使用AI的凭证，请务必妥善保管他。）

- API_url: 选择合适的模型，找到他的POST请求地址(也就是API_url)，如果你选择的是v3，那么地址如下：`https://api.siliconflow.cn/v1/chat/completions`

## bilibili live

在此模块需要获取的内容有：

1. 你的直播间的房间号 ROOMID 

如果你的直播间的链接是`https://live.bilibili.com/1732028631` ，那么`ROOMID = 1732028631 `

2. 你的bilibili账号UID

如果你的个人主页的链接是`https://space.bilibili.com/381771544` ，那么`UID = 381771544`

3. cookies

在浏览器中打开你的直播间页面，按F12，找到“应用”(火狐浏览器为storage)，

找到cookies,复制`SESSDATA`和`bili_jct`

<img src=".\screenshots\cookies.png" alt="image-20250502224838529" style="zoom:50%;" />

## 配置config.py

将`config_tmp.py` 改名为`config.py`

按照你的需求配置config.py。

并将前几个小节中获得的如API keys，ROOMID，UID，sessdata和bili_jct写入config.py中。

## 运行danmu2voice

到此位置，便完成了所有的配置过程，下面是启动过程：

1. 首先运行GPT-SoVITS：运行GPT-SoVITS项目文件中的`api.py` （注意修改路径）:

```sh
D:/0file/projs/GPT-SoVITS-v3lora-20250228/runtime/python.exe "D:/0file/projs/GPT-SoVITS-v3lora-20250228/api.py" -dr "D:/0file/projs/GPT-SoVITS-v3lora-20250228/voice/paiMeng/说话-既然罗莎莉亚说足迹上有元素力，用元素视野应该能很清楚地看到吧。.wav" -dt "既然罗莎莉亚说足迹上有元素力，用元 素视野应该能很清楚地看到吧。" -dl "zh"
```

2. 运行danmu2voice项目中的main.py

```sh
python ./main.py
```



