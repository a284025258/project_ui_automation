from abc import ABCMeta, abstractmethod


class ABCAuthAPIBase(metaclass=ABCMeta):
    """
    鉴权接口抽象基类
    需要实现
    属性: [path,]
    方法: [_send(),]

    """

    @abstractmethod
    def _send(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def path(self):
        pass
