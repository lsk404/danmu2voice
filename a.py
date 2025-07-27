from bilibili_api import live, sync
import json
room = live.LiveDanmaku(1732028631)

@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    # print(event)
    extra = json.loads(event['data']['info'][0][15]['extra'])
    msg = extra['content']
    face_url = event['data']['info'][0][15]['user']['base']['face']
    uname = event['data']['info'][0][15]['user']['base']['name']
    
@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    print(event)
if __name__ == '__main__':
    sync(room.connect())


