
class SpamChannel:
    guildId: int
    channelId: int

    def __init__(self, guildId=None, channelId=None):
        self.guildId = guildId
        self.channelId = channelId

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
