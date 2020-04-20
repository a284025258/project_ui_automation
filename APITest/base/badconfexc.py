class BadConfException(BaseException):
    """
    错误的配置
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return "place check configuration file"
