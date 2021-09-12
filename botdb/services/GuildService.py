from botdb.entities.Guild import Guild
from botdb.repository import GuildRep as Repos
from botdb.services import LevelRoleService


# ====ADD============================
# Создаёт новую запись с guild_id
def add_new_guild(guildId: int):
    Repos.init_new_guild(guildId=guildId)


# ====GET============================
# Извлекает все данные связанные с переданным guildId (список уровней не подгружается)
def get_guild_by_guild_id(guildId: int):
    row = Repos.get_guild_by_guild_id(guildId=guildId)
    if row is None:
        raise ValueError('GuildService.get_guild_by_guild_id(): returned row is null')
    return Guild(guildId=row[0], maxLinks=row[1], muteTime=row[2], personalRolesAllowed=row[3],
                 banBotFunctions=row[4], noLinksRoleId=row[5], lightMuteRoleId=row[6], muteRoleId=row[7],
                 muteVoiceChatRoleId=row[8], CHIELDChatId=row[9], CHIELDWarningCount=row[10],
                 CHIELDAlertCount=row[11], voiceChatCreatorId=row[12], membersCounterChatId=row[13],
                 rolesCounterChatId=row[14], welcomePhrase=row[15], welcomeGifGroupId=row[16])


# Возвращает все записи в таблице
def get_all_guilds():
    rows = Repos.get_all_guilds()
    guildList = []
    for row in rows:
        guild = Guild(guildId=row[0], maxLinks=row[1], muteTime=row[2], personalRolesAllowed=row[3],
                      banBotFunctions=row[4], noLinksRoleId=row[5], lightMuteRoleId=row[6], muteRoleId=row[7],
                      muteVoiceChatRoleId=row[8], CHIELDChatId=row[9], CHIELDWarningCount=row[10],
                      CHIELDAlertCount=row[11], voiceChatCreatorId=row[12], membersCounterChatId=row[13],
                      rolesCounterChatId=row[14], welcomePhrase=row[15], welcomeGifGroupId=row[16])
        guildList.append(guild)
    return guildList


# Возвращает количество записей в таблице
def get_guilds_count():
    return Repos.get_guilds_count()[0]


# Возвращает словарь всех серверов с заполненным levelsMap {level[int]: levelRole}
def get_guild_boot_setup():
    guilds = get_all_guilds()
    answer = {}

    for guild in guilds:
        levelRoles = LevelRoleService.get_level_roles_dict_by_guild_id(guildId=guild.guildId)
        rolesDict = {levelRoles[key].level: levelRoles[key].roleId for key in levelRoles.keys()}
        guild.levelsMap = rolesDict
        answer[guild.guildId] = guild

    return answer


# ====UPDATE============================
# Обновляет все поля в таблице связанные с guildId
def update_guild_full(guild: Guild):
    Repos.update_guild_full(guild=guild)


# Обновляет поля max_links, mute_time, personal_roles_allowed
def update_guild_common(guild: Guild):
    Repos.update_guild_common(guild=guild)


# Обновляет поля ban_bot_functions, no_links_role_id, light_mute_role_id, mute_role_id, mute_voice_chat_role_id
def update_guild_roles(guild: Guild):
    Repos.update_guild_roles(guild=guild)


# Обновляет поля CHIELD_chat_id, CHIELD_warning_count, CHIELD_alert_count
def update_guild_shield_settings(guild: Guild):
    Repos.update_guild_shield_settings(guild=guild)


# Обновляет поля voice_chat_creator_id, members_counter_chat_id, roles_counter_chat_id
def update_guild_chats(guild: Guild):
    Repos.update_guild_chats(guild=guild)


# Обновляет поле welcome_phrase
def update_guild_welcome_phrase(guild: Guild):
    Repos.update_guild_welcome_phrase(guild=guild)


# Обновляет поле gif_group_id
def update_welcome_gif_group_id(guild: Guild):
    Repos.update_welcome_gif_group_id(guild=guild)


# ====DELETE============================
# удаляет запись с указанным guildId
def delete_guild_by_guild_id(guildId: int):
    Repos.delete_guild_by_guild_id(guildId=guildId)


def clear_table():
    Repos.clear_table()
