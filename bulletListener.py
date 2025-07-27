import threading
import asyncio
from bilibili_api import live, sync
import json
import time

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mylog import logger
def log(txt):
    with open("log.txt", "w+") as f:
        f.write(txt)
class DanmuListener:
    def __init__(self, room_id,callback=None):
        self.room_id = room_id
        self.callback = callback
        self._running = False
        self._monitor = None
        self._retry_count = 0

    async def _connect(self):
        while self._running:
            try:
                # 创建新连接实例
                self._monitor = live.LiveDanmaku(1732028631)
                self._monitor.add_event_listener("DANMU_MSG", self.on_danmu)
                await self._monitor.connect()
                self._retry_count = 0  # 重置重试计数器
                return
            except Exception as e:
                logger.error(f"连接异常: {e}, 5秒后重试...")
                self._retry_count += 1
                await asyncio.sleep(5)

    async def _keep_connected(self):
        while self._running:
            await self._connect()
            # 等待连接断开
            while self._running and self._monitor.get_status() < 4:
                # 0 初始化，1 连接建立中，2 已连接，3 断开连接中，4 已断开，5 错误
                await asyncio.sleep(1)

    async def on_danmu(self, event):
        extra = json.loads(event['data']['info'][0][15]['extra'])
        msg = extra['content']
        face_url = event['data']['info'][0][15]['user']['base']['face']
        uname = event['data']['info'][0][15]['user']['base']['name']
        if self.callback:
            self.callback(msg, uname, face_url)

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
    from config import ROOMID,credential_sessdata,credential_bili_jct,UID

    # 创建监听器（保持原有接口不变）
    listener = DanmuListener(ROOMID, 
                           callback=lambda msg,uname,face_url: print(f"[{uname}]: {msg}"))
    listener.start()
    logger.info("弹幕监听已启动，主线程继续运行...")

    try:
        while True:
            user_input = input("输入 'exit' 退出: ")
            if user_input == "exit":
                break
    finally:
        listener.stop()
        logger.info("弹幕监听已停止")

"""
小青蛙发送Text to send:
{
    'room_display_id': 1732028631, 
    'room_real_id': 1732028631, 
    'type': 'DANMU_MSG', 
    'data': {
        'cmd': 'DANMU_MSG', 
        'dm_v2': '', 
        'info': [
            [0, 1, 25, 16777215, 1753633024998, 1753633024806, 0,
            '535ee2e9', 0, 0, 0, '', 0, '{}', '{}', 
                {   'extra': 
                    '{
                        "send_from_me":false,
                        "master_player_hidden":false,
                        "mode":0,
                        "color":16777215,
                        "dm_type":0,
                        "font_size":25,
                        "player_mode":1,
                        "show_player_type":0,
                        "content":"Text to send",
                        "user_hash":"1398727401",
                        "emoticon_unique":"",
                        "bulge_display":0,
                        "recommend_score":1,
                        "main_state_dm_color":"",
                        "objective_state_dm_color":"",
                        "direction":0,
                        "pk_direction":0,
                        "quartet_direction":0,
                        "anniversary_crowd":0,
                        "yeah_space_type":"",
                        "yeah_space_url":"",
                        "jump_to_url":"",
                        "space_type":"",
                        "space_url":"",
                        "animation":{},
                        "emots":null,
                        "is_audited":false,
                        "id_str":"1f35b391801e193704542a1fe06886517325",
                        "icon":null,
                        "show_reply":true,
                        "reply_mid":0,
                        "reply_uname":"",
                        "reply_uname_color":"",
                        "reply_is_mystery":false,
                        "reply_type_enum":0,
                        "hit_combo":0,
                        "esports_jump_url":""
                    }', 
                    'mode': 0, 
                    'show_player_type': 0, 
                    'user': {
                        'base': {
                            'face': 'https://i1.hdslb.com/bfs/face/7ead047a9a5cbc4e66071f422c0deba2bdc69c17.jpg', 
                            'is_mystery': False, 
                            'name': '小***', 
                            'name_color': 0, 
                            'name_color_str': '', 
                            'official_info': {
                                'desc': '', 
                                'role': 0,
                                'title': '',
                                'type': -1
                            },
                            'origin_info': {
                                'face': 'https://i1.hdslb.com/bfs/face/7ead047a9a5cbc4e66071f422c0deba2bdc69c17.jpg',
                                'name': '小***'
                            }, 
                            'risk_ctrl_info': None
                        }, 
                        'guard': None, 
                        'guard_leader': {
                            'is_guard_leader': False
                        }, 
                        'medal': None, 
                        'title': {
                            'old_title_css_id': '', 
                            'title_css_id': ''
                        }, 
                        'uhead_frame': None, 
                        'uid': 0, 
                        'wealth': {
                            'dm_icon_key': '',
                            'level': 1
                        }
                    }
                }, 
                {
                    'activity_identity': '', 
                    'activity_source': 0,
                    'not_show': 0
                }, 
                0
            ], 
            'ABCD', 
            [0, '小***', 0, 0, 0, 10000, 1, ''], 
            [], 
            [0, 0, 9868950, '>50000', 0], 
            ['', ''], 
            0, 0, None, 
            {
                'ct': '89021F90',
                'ts': 1753633024},
            0, 0, None, None, 0, 260, [1], None
        ]
    }
}
"""