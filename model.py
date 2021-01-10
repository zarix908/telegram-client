from collections import defaultdict
from queue import Queue


class Model:
    def __init__(self):
        self.__chats = defaultdict(Queue)
