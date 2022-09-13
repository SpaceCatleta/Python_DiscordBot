import datetime

from botdb.entities.ActivityLog import ActivityLog
from botdb.repository import ActivityLogRep as Repos



def getByPrimaryKey(guildId: int, userId: int, period: datetime.date):
    return Repos.get_by_primary_key(guildId=guildId, userId=userId, period=period)


def logOneMessage(guildId: int, userId: int, period: datetime.date, symbolsCount: int):
    entity: ActivityLog = Repos.get_by_primary_key(guildId=guildId, userId=userId, period=period)
    isNew = False
    if entity is None:
        isNew = True
        entity = ActivityLog()
        entity.guildId = guildId
        entity.userId = userId
        entity.period = period



    entity.symbolsCount += symbolsCount
    entity.messagesCount += 1

    if isNew:
        Repos.add(entity=entity)
        # print("logged new")
    else:
        Repos.update(entity=entity)
        # print("update log")



def logOneSpamMessage(guildId: int, userId: int, period: datetime.date, symbolsCount: int):
    entity: ActivityLog = Repos.get_by_primary_key(guildId=guildId, userId=userId, period=period)
    isNew = False
    if entity is None:
        isNew = True
        entity = ActivityLog()
        entity.guildId = guildId
        entity.userId = userId
        entity.period = period

    entity.spamSymbolsCount += symbolsCount
    entity.spamMessagesCount += 1

    if isNew:
        Repos.add(entity=entity)
        # print("spam logged new")
    else:
        Repos.update(entity=entity)
        # print("spam update log")


def logVoiceChatTime(guildId: int, userId: int, period: datetime.date, periodTime: datetime.time, chatTime: int):
    entity: ActivityLog = Repos.get_by_primary_key(guildId=guildId, userId=userId, period=period)
    isNew = False
    if entity is None:
        isNew = True
        entity = ActivityLog()
        entity.guildId = guildId
        entity.userId = userId
        entity.period = period

    entity.voiceChatTime += int(chatTime * 10) / 10

    currTimeSeconds = periodTime.second + periodTime.minute * 60 + periodTime.hour * 3600

    if currTimeSeconds < entity.voiceChatTime:
        logVoiceChatTime(guildId=guildId, userId=userId,
                         period=period - datetime.timedelta(days=1), periodTime=datetime.time(hour=23, minute=59),
                         chatTime=chatTime-currTimeSeconds)
        entity.voiceChatTime += currTimeSeconds - int(chatTime * 10) / 10
    if isNew:
        Repos.add(entity=entity)
        # print("voice logged new")
    else:
        Repos.update(entity=entity)
        # print("voice update log")


def get_afk_users_id_after_date(guild_id: int, daysToCheck: int, guildMembersIdList) -> tuple:
    date = datetime.datetime.utcnow() - datetime.timedelta(days=daysToCheck)
    date = datetime.datetime.strftime(date, "%Y-%m-%d")

    id_list = Repos.get_active_users_id_after_date(guild_id=guild_id, date=date)
    print(f'all non afk users count:   {len(id_list)}')
    print(id_list)
    return tuple(filter(lambda val: val not in id_list, guildMembersIdList))
