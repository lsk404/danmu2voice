import threading
import asyncio
from bilibili_api import Credential, sync
from bilibili_api.live import LiveDanmaku
import time

class DanmuListener:
    def __init__(self, room_id, credential, callback=None):
        self.room_id = room_id
        self.credential = credential
        self.callback = callback
        self.uid = 381771544
        self._running = False
        self._monitor = None
        self._retry_count = 0

    async def _connect(self):
        while self._running:
            try:
                # 创建新连接实例
                self._monitor = LiveDanmaku(self.room_id, credential=self.credential)
                self._monitor.add_event_listener("DANMU_MSG", self.on_danmu)
                await self._monitor.connect()
                self._retry_count = 0  # 重置重试计数器
                return
            except Exception as e:
                print(f"连接异常: {e}, 5秒后重试...")
                self._retry_count += 1
                await asyncio.sleep(5)

    async def _keep_connected(self):
        while self._running:
            await self._connect()
            # 等待连接断开
            while self._running and self._monitor.connected:
                await asyncio.sleep(1)

    async def on_danmu(self, event):
        uname = event["data"]["info"][2][1]
        msg = event["data"]["info"][1]
        if self.callback:
            self.callback(msg, uname)

    def start(self):
        if self._running:
            return
            
        self._running = True
        
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._keep_connected())

        # 在独立线程中运行异步循环
        self._thread = threading.Thread(target=run_async, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._monitor:
            sync(self._monitor.disconnect())


if __name__ == "__main__":
    ROOMID = 1732028631
    credential = Credential(
        sessdata="2860b4ca%2C1759585710%2C4530d%2A41CjDGyNDV0ViIhZkt73f_t_vOaPFyDFo8rksfYKE90lGf6quVj38a4EukhlKtVMHK7XMSVjRjRFNOQl81Q1Z2aFFCVjhuTm14cEoyQW1NM0JLbWRvZjdvTmVYVlEyd0lyY0Q4WUg3VEpYRlZOdlE3NnNQWlBFbHgxNnVLRG1YQmd4TlZlRnFrSHpBIIEC",
        bili_jct="f1f7cbd5832b7ddcd355f901b3b93fcc"
    )

    # 创建监听器（保持原有接口不变）
    listener = DanmuListener(ROOMID, credential, 
                           callback=lambda msg, uname: print(f"[{uname}]: {msg}"))
    listener.start()
    print("弹幕监听已启动，主线程继续运行...")

    try:
        while True:
            user_input = input("输入 'exit' 退出: ")
            if user_input == "exit":
                break
    finally:
        listener.stop()
        print("弹幕监听已停止")