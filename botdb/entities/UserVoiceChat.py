
class UserVoiceChat:
    userId: int
    chatName: str
    maxUsersCount: int

    def __init__(self, userId=None, chatName=None, maxUsersCount=None):
        self.userId = userId
        self.chatName = chatName
        self.maxUsersCount = maxUsersCount

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
