from abc import abstractmethod, ABCMeta

from requests.auth import AuthBase


class ABCTokenAuth(AuthBase, metaclass=ABCMeta):
    """
    用单例模式-改实现的
    token鉴权的抽象基类
    实现了
    重复请求控制
    token缓存
    """
    _objs = None

    def __new__(cls, *args, **kwargs):
        if cls._objs is None:
            cls._objs = {}

        if args not in cls._objs:
            instance = super().__new__(cls)
            cls._objs[args] = instance
            return instance
        else:
            return cls._objs[args]

    def __init__(self, *args, **kwargs):
        """
        :param role_name:
        """
        self._token = None
        self.args = args
        self.kwargs = kwargs

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
