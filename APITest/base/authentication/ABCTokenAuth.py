import threading
from abc import abstractmethod, ABCMeta

from requests.auth import AuthBase


class ABCTokenAuth(AuthBase, metaclass=ABCMeta):
    """
    单例模式模式-改
    token鉴权的抽象基类
    实现了
    重复请求控制
    token缓存
    """
    _instance_lock = threading.Lock()
    _instances = None

    def __new__(cls, role_name, *args, **kwargs):
        with ABCTokenAuth._instance_lock:

            if cls._instances is None:
                cls._instances = {}

            if role_name not in cls._instances:
                instance = super().__new__(cls)
                instance._flag = True
                cls._instances[role_name] = instance
                return instance
            else:
                return cls._instances[role_name]

    def __init__(self, role_name, *args, **kwargs):
        """
        :param role_name:
        """
        if self._flag:
            self._token = None
            self.args = args
            self.kwargs = kwargs
            self.role_name = role_name
            self._flag = False

    def __call__(self, r):
        r.headers['token'] = self.token
        return r

    @property
    def token(self):
        if self._token:
            return self._token
        else:
            self._token = self._get_token()
            return self._token

    @abstractmethod
    def _get_token(self):
        pass
