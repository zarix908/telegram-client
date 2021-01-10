import asyncio
import time
from collections import defaultdict

start = time.time()


def ctime():
    diff = (time.time() - start)
    return int(round(
        diff * 1000
    ))


def read_event():
    t = ctime()

    if t > 10000:
        return {'type': 'sent', 'value': 2}
    if t > 2000:
        return {'type': 'login', 'value': 1}

    return None


class Client:
    def __init__(self, event_loop=None):
        if not event_loop:
            event_loop = asyncio.get_event_loop()
        self.__event_loop = event_loop

        self.__futures = defaultdict(list)
        self.__event_loop.call_soon(self.__step)
        self.__bind_methods()

    def __step(self):
        self.__event_loop.call_soon(self.__step)

        event = read_event()
        if not event:
            return
        for event_type, futures in self.__futures.items():
            if event['type'] != event_type:
                continue
            for future in futures:
                future.set_result(event['value'])

        if event['type'] in self.__futures:
            self.__futures.pop(event['type'])

    def __bind_methods(self):
        self.login = self.__create_method('login')
        self.send_message = self.__create_method('sent')

    def __create_method(self, event_type):
        def func():
            f = asyncio.Future()
            self.__futures[event_type].append(f)

            return f

        return func


async def main():
    c = Client()
    r = await c.login()
    print(f'login {ctime()} {r}')
    r = await c.send_message()
    print(f'sent {ctime()} {r}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
