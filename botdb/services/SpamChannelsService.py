from botdb.entities.SpamChannel import SpamChannel
from botdb.repository import SpamChannelsRep as Repos


# ====ADD============================
def add(spamChannel: SpamChannel):
    Repos.add(spamChannel)


def add2(guildId: int, channelId: int):
    Repos.add(SpamChannel(guildId=guildId, channelId=channelId))


# ====GET============================
def is_exist(guildId: int, channelId: int):
    return Repos.get_by_id(guildId=guildId, channelId=channelId) is not None


def get_by_id(guildId: int, channelId: int):
    return Repos.get_by_id(guildId=guildId, channelId=channelId)


def get_by_guild_id(guildId: int):
    return Repos.get_by_guild_id(guildId)


def get_id_list_by_guild_id(guildId: int):
    return Repos.get_id_list_by_guild_id(guildId)


def get_count():
    return Repos.get_count()


def get_all():
    return Repos.get_all()


# ====DELETE============================
def delete_by_id(guildId: int, channelId: int):
    Repos.delete_by_id(guildId=guildId, channelId=channelId)


def clear_table():
    Repos.clear_table()
