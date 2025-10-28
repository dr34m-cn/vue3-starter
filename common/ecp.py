class Ecp(Exception):
    def __init__(self, message, code=500):
        """
        异常
        :param message: 错误消息
        :param code: 错误代码
        """
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return self.message
