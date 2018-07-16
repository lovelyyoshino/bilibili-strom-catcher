from random import random
import math


def random_user_id():
    return pow(10, 15) + int(math.floor(2 * pow(10, 15) * random()))
