import threading
from bilibili_api import Credential, sync
from bilibili_api.live import LiveDanmaku

class DanmuListener:
    def __init__(self, room_id, credential, callback=None):
        self.room_id = room_id
        self.credential = credential
        self.monitor = LiveDanmaku(room_id, credential=credential)
        self.uid = 381771544  # 替换成你的UID
        self.callback = callback

    async def on_danmu(self, event):
        uname = event["data"]["info"][2][1]
        msg = event["data"]["info"][1]
        # print(event["data"]["info"])
        if self.callback:
            self.callback(msg,uname)

    def start(self):
        self.monitor.add_event_listener("DANMU_MSG", self.on_danmu)
        sync(self.monitor.connect())  # 这里会阻塞


if __name__ == "__main__":
    # 主线程继续执行其他任务
    ROOMID = 1732028631
    credential = Credential(
        sessdata="2860b4ca%2C1759585710%2C4530d%2A41CjDGyNDV0ViIhZkt73f_t_vOaPFyDFo8rksfYKE90lGf6quVj38a4EukhlKtVMHK7XMSVjRjRFNOQl81Q1Z2aFFCVjhuTm14cEoyQW1NM0JLbWRvZjdvTmVYVlEyd0lyY0Q4WUg3VEpYRlZOdlE3NnNQWlBFbHgxNnVLRG1YQmd4TlZlRnFrSHpBIIEC",
        bili_jct="f1f7cbd5832b7ddcd355f901b3b93fcc"
    )
    # 创建监听器
    listener = DanmuListener(ROOMID, credential)
    listener.start()
    print("弹幕监听已启动，主线程继续运行...")
    while True:
        user_input = input("输入 'exit' 退出: ")
        if user_input == "exit":
            break