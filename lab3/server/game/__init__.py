from abc import ABCMeta
from importlib import import_module
from threading import Thread

from common.message import Message
from common.socket_wrapper import SocketWrapper


class ServerGame(Thread, metaclass=ABCMeta):
    def __init__(self, user: SocketWrapper):
        super().__init__()
        self._user = user


class GameChooser(Message):
    def __init__(self, class_):
        module_name = class_.__module__
        class_name = class_.__name__
        super().__init__((module_name, class_name))

    @property
    def payload(self):
        module_name, class_name = super().payload
        module = import_module(module_name)
        class_ = getattr(module, class_name)
        return class_
