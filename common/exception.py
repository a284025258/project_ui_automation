class TestAZException(Exception):
    """
    异常基类
    """

    def __init__(self, msg=None):
        self.msg = msg


class BadConfException(TestAZException):
    """
    错误的配置
    """
    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return "place check configuration file"
