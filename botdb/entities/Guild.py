
class Guild:
    guildId: int
    maxLinks: int
    muteTime: int
    personalRolesAllowed: int
    banBotFunctions: int
    noLinksRoleId: int
    lightMuteRoleId: int
    muteRoleId: int
    muteVoiceChatRoleId: int
    CHIELDChatId: int
    CHIELDWarningCount: int
    CHIELDAlertCount: int
    voiceChatCreatorId: int
    membersCounterChatId: int
    rolesCounterChatId: int
    welcomePhrase: int
    welcomeGifGroupId: int
    levelsMap: dict

    def __init__(self, guildId=None, maxLinks=None, muteTime=None, personalRolesAllowed=None, banBotFunctions=None,
                 noLinksRoleId=None, lightMuteRoleId=None, muteRoleId=None, muteVoiceChatRoleId=None, CHIELDChatId=None,
                 CHIELDWarningCount=None, CHIELDAlertCount=None, voiceChatCreatorId=None, membersCounterChatId=None,
                 rolesCounterChatId=None, welcomePhrase=None, welcomeGifGroupId=None):
        self.guildId = guildId
        self.maxLinks = maxLinks
        self.muteTime = muteTime
        self.personalRolesAllowed = personalRolesAllowed
        self.banBotFunctions = banBotFunctions
        self.noLinksRoleId = noLinksRoleId
        self.lightMuteRoleId = lightMuteRoleId
        self.muteRoleId = muteRoleId
        self.muteVoiceChatRoleId = muteVoiceChatRoleId
        self.CHIELDChatId = CHIELDChatId
        self.CHIELDWarningCount = CHIELDWarningCount
        self.CHIELDAlertCount = CHIELDAlertCount
        self.voiceChatCreatorId = voiceChatCreatorId
        self.membersCounterChatId = membersCounterChatId
        self.rolesCounterChatId = rolesCounterChatId
        self.welcomePhrase = welcomePhrase
        self.welcomeGifGroupId = welcomeGifGroupId
        self.levelsMap = {}

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
