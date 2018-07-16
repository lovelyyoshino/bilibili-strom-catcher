import logging
import aiohttp
import asyncio
import requests
import json
import time
import datetime
from http import cookies
from threading import Thread
from pybililive.handler import danmmu_msg
from pybililive.consts import (
    LIVE_BASE_URL, SEND_DANMU_URI
)
import login

logger = logging.getLogger('bili')


def build_cookie_with_str(cookie_str):
    simple_cookie = cookies.SimpleCookie(Cookie_check())  # Parse Cookie from str
    cookie = {key: morsel.value for key, morsel in simple_cookie.items()}
    return cookie

def Cookie_check():
    try:
        
        lo = login.Login('','')
        lo.logining()
        cookie_str = str(lo.cookies)
    except Exception as e:
        pass
    finally:
        tmp2=''
        return tmp2
        #return file_cookies
danmu_url = r'http://{host}:{port}/{uri}'.format(
    host=LIVE_BASE_URL,
    port=80,
    uri=SEND_DANMU_URI
)

user_session = requests.session()


def keep_session():
    while True:

        try:

            global user_session
            user_session.get(
                url='http://live.bilibili.com/User/getUserInfo',
                headers={'Cookie': Cookie_check()}
            )
            time.sleep(300)
            logger.debug('Keep session alive.')
        except Exception as e:
            pass


keep_alive_thread = Thread(target=keep_session)
keep_alive_thread.setDaemon(True)
keep_alive_thread.start()

async def send_danmu(danmu, room_id, color=16777215, font_size=25, mode='1'):
    check_url = 'https://api.live.bilibili.com/lottery/v1/Storm/check?roomid=%s'%room_id
    res = requests.get(url=check_url).json()
    join_id = res['data']['id']
    
    
    url = 'https://api.live.bilibili.com/lottery/v1/Storm/join'
    data = {
        'id':join_id
    }
    header = {'Cookie':Cookie_check()}
    await asyncio.sleep(0.2)
    res = requests.post(url,headers = header,data=data).json()
    print('房间%s触发节奏风暴'%room_id)
    with open('节奏风暴log.txt','a+') as f:
        if res['code']==0:
            r_data = '%s  id:%s领取成功%s\n'%(datetime.datetime.now(),join_id,res['data']['mobile_content'])
            f.write(r_data)
            #print(r_data)
            print(join_id,res['data']['mobile_content'])
        else:
            r_data = '%s  id:%s领取失败%s\n'%(datetime.datetime.now(),join_id,res)
            f.writelines(r_data)
            #print(r_data)
            print(join_id,'领取失败:',res['msg'])
            #f.write(join_id,'领取失败:',res['msg'])
    
    # try:
    #     global user_session
    #     res = user_session.post(
    #         url=danmu_url,
    #         headers={'Cookie': Cookie_check()},
    #         data={
    #             'msg': danmu,
    #             'color': color,
    #             'fontsize': font_size,
    #             'roomid': room_id,
    #             'mode': mode,
    #             'rnd': int(time.time())
    #         }
    #     )

    #     data = json.loads(res.text)
        
    #     if data['msg']:
    #         logging.exception(data)
    #         raise Exception(data['msg'])

    # except Exception as e:
    #     logger.exception(e)
    #     logger.error('房间{} 弹幕 {} 发送失败'.format(room_id, danmu))
    # else:
    #     logger.info('房间{}  弹幕 {} 发送成功'.format(room_id, danmu))
    # finally:
    #     return


async def special_gift(live_obj, message):
    try:
        content = message['data'].get('39', {}).get('content')
        if content:
            await send_danmu(content, room_id=live_obj.room_id)
            #logger.info('参与房间 {} 节奏风暴'.format(live_obj.room_id))
    except Exception as e:
        logger.exception(e)


async def sys_gift(live_obj, message):
    try:

        if message.get('giftId') == 39:
            res = await aiohttp.request(
                'GET',
                r'http://api.live.bilibili.com/SpecialGift/room/{}'.format(message['roomid'])
            )
            data = await res.json()
            content = data['data'].get('gift39', {}).get('content')
            if content:
                await send_danmu(content, room_id=message['roomid'])
                logger.info('参与房间 {} 节奏风暴'.format(live_obj.room_id))
    except Exception as e:
        logger.exception(e)


async def check_special_gift(live_obj, message):
    try:
        content = message['data'].get('39', {}).get('content')
        if content:
            live_obj.set_cmd_func('DANMU_MSG', danmmu_msg)
            await asyncio.sleep(5)
            live_obj.set_cmd_func('DANMU_MSG', None)
    except Exception as e:
        logger.exception(e)


async def check_sys_gift(live_obj, message):
    try:

        if message.get('giftId') == 39:
            res = await aiohttp.request(
                'GET',
                r'http://api.live.bilibili.com/SpecialGift/room/{}'.format(message['roomid'])
            )
            data = await res.json()
            logging.INFO('获取到的数据：%s'%data)
            content = data['data'].get('gift39', {}).get('content')
            if content:
                live_obj.set_cmd_func('DANMU_MSG', danmmu_msg)
                await asyncio.sleep(5)
                live_obj.set_cmd_func('DANMU_MSG', None)
    except Exception as e:
        logger.exception(e)


cmd_func = {
    'SPECIAL_GIFT': special_gift,
    'SYS_GIFT': sys_gift,
    # 'DANMU_MSG': danmmu_msg
}
