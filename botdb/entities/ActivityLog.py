from datetime import datetime


class ActivityLog:
    guildId:  int
    userId: int
    period: datetime.date
    messagesCount: int
    symbolsCount: int
    voiceChatTime: int
    spamMessagesCount: int
    spamSymbolsCount: int

    def __init__(self):

        self.guildId = 0
        self.userId = 0
        self.period = None
        self.messagesCount = 0
        self.symbolsCount = 0
        self.voiceChatTime = 0
        self.spamMessagesCount = 0
        self.spamSymbolsCount = 0


    @staticmethod
    def from_row(row):
        ans = ActivityLog()
        ans.guildId = row[0]
        ans.userId = row[1]
        ans.period = row[2]
        ans.messagesCount = row[3]
        ans.symbolsCount = row[4]
        ans.voiceChatTime = row[5]
        ans.spamMessagesCount = row[6]
        ans.spamSymbolsCount = row[7]

        return ans


    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
