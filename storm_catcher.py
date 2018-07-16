import multiprocessing
from taskscreator import Taskcreator
import asyncio
import logging.config
from get_hot_room_ids import get_room_ids
import time

logging.config.fileConfig("logger.conf")


def start_catcher(page):
    room_ids = get_room_ids(page)
    creator = Taskcreator(rooms=room_ids)

    asyncio.ensure_future(creator.creating())

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    try:
        loop.run_forever()
    except Exception as e:
        logging.exception(e)
        for task in asyncio.Task.all_tasks():
            task.cancel()
        loop.run_forever()

    loop.close()
def sleeptime(hour):
    return hour*3600
def run():
    pool = multiprocessing.Pool(processes=12)
    for page in range(1, 12):
        pool.apply_async(start_catcher, (page,))
    pool.close()
    src = sleeptime(1)
    time.sleep(src)
    pool.terminate()
    pool.join()
    
if __name__ == '__main__':
    
    while True:
        run()
        
        
        
        

        
