from datetime import datetime as DateTime


class GuildMember:
    userId: int
    guildId: int
    personalRoleId: int
    visitsCount: int
    warningsCount: int
    banBotFunctions: int
    punishmentRoleId: int
    punishmentEndDate: DateTime

    def __init__(self, userId=None, guildId=None, personalRoleId=None, visitsCount=None,
                 warningsCount=None, banBotFunctions=None, punishmentRoleId=None, punishmentEndDate=None):
        self.userId = userId
        self.guildId = guildId
        self.personalRoleId = personalRoleId
        self.visitsCount = visitsCount
        self.warningsCount = warningsCount
        self.punishmentRoleId = punishmentRoleId
        self.punishmentEndDate = punishmentEndDate
        self.banBotFunctions = banBotFunctions

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
