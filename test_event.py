import unittest
from unittest.mock import Mock

from event import Event


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.__event = Event()
        self.__listener = Mock(return_value=None)

    def test_add_listener(self):
        self.__event += self.__listener
        self.__event()

        self.__listener.assert_called_once()

    def test_remove_listener(self):
        self.__event += self.__listener
        self.__event -= self.__listener
        self.__event()

        self.__listener.assert_not_called()

    def test_pass_args_to_listener(self):
        args = [1, 'str1', ()]
        kwargs = {'arg1': 'str2', 'arg2': []}

        self.__event += self.__listener
        self.__event(*args, **kwargs)

        self.__listener.assert_called_once_with(*args, **kwargs)

    def test_call_all_listeners(self):
        listeners = [Mock(return_value=None) for i in range(5)]

        for listener in listeners:
            self.__event += listener
        self.__event()

        for listener in listeners:
            listener.assert_called_once()
