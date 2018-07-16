import logging
import asyncio
from pybililive.bililive import BiliLive
import handler

logger = logging.getLogger('bili')


class Taskcreator(object):
    __slots__ = ['tasks', 'rooms']

    def __init__(self, rooms):
        self.tasks = {}
        self.rooms = rooms

    async def creating(self):
        for room in self.rooms:
            danmuji = BiliLive(room, cmd_func_dict=handler.cmd_func)
            task = asyncio.ensure_future(danmuji.connect())
            self.tasks[room] = task
            await asyncio.sleep(0.1)

        while True:
            await asyncio.sleep(10)
            for room, task in self.tasks.items():
                if task.done():
                    task.cancel()
                    logging.info('重新进入直播间 %s' % room)
                    logging.debug('reenter %s' % room)
                    danmuji = BiliLive(room, cmd_func_dict=handler.cmd_func)
                    task = asyncio.ensure_future(danmuji.connect())
                    self.tasks[room] = task
            logging.debug('len: %s' % len(self.tasks))
            logging.debug('now there is %s' % len(asyncio.Task.all_tasks()))
