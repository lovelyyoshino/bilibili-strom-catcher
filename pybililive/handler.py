import collections
import datetime

Danmu = collections.namedtuple(
    'Danmu',
    ['danmu_header', 'content', 'user_info', 'user_badge', 'user_level', 'user_title', 'user_is_vip', 'user_is_svip']
)


async def danmmu_msg(live, message):
    danmu = Danmu(*message['info'])
    print('{} {} 说: {}'.format(
        datetime.datetime.fromtimestamp(danmu.danmu_header[4]),
        danmu.user_info[1],
        danmu.content)
    )


async def send_gift(live, message):
    user_name = message['data']['uname']
    gift_name = message['data']['giftName']
    num = message['data']['num']
    print('{} 送出了 {}x{}'.format(user_name, gift_name, num))
