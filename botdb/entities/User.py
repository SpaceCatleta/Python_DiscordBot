
class User:
    userId: int
    exp: float
    level: int
    messagesCount: int
    symbolsCount: int
    voiceChatTime: int
    voluteCount: int
    expModifier: int

    def __init__(self, userId=None, exp=None, level=None, messagesCount=None, symbolsCount=None, voiceChatTime=None,
                 voluteCount=None, expModifier=None):
        self.userId = userId
        self.exp = exp
        self.level = level
        self.messagesCount = messagesCount
        self.symbolsCount = symbolsCount
        self.voiceChatTime = voiceChatTime
        self.voluteCount = voluteCount
        self.expModifier = expModifier

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
