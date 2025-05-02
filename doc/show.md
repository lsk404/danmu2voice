# danmu2voice 效果展示

## 窗口页面

运行danmu2voice中的`main.py` 后会创建一个可拖动的，置顶的灰色窗口（窗口样式可以在`window.py` 文件中更改）

<img src="./screenshots/window.png" alt="window" style="zoom: 50%;" />



并在任务栏折叠区打开一个小图标。

![image-20250502231444183](./screenshots/taskbar.png)

右键/双击它可以切换窗口的状态（隐藏or显示）

右键可以退出danmu2voice程序。

在接收到一个弹幕后，窗口会显示当前处理的弹幕，以及AI的回复。

<img src="./screenshots/talk_window.png" alt="image-20250502231444183" style="zoom: 50%;" />

## 命令行

在danmu2voice的命令行中直接输入文本会让AI照着念（不通过LLM得到回复）。

danmu2voice程序的命令行显示如下：

<img src="./screenshots/danmu2voice_shell.png" alt="image-20250502231444183" style="zoom: 50%;" />

GPT-SoVITS命令行显示如下：

<img src="./screenshots/GPT-SoVITS.png" alt="image-20250502231444183" style="zoom: 50%;" />

