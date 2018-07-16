import requests
import json
import time


def get_room_ids(page):
    time.sleep(1)
    url = 'http://api.live.bilibili.com/area/liveList'
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection':'keep-alive',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
              }
    response = requests.get(url,headers=headers, params={'area': 'all', 'order': 'online', 'page': page})
    data = json.loads(response.text)
    room_ids = []
    if data['code'] == 0:
        room_ids = [each['roomid'] for each in data['data']]
    return room_ids

