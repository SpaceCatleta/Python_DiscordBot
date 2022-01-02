import discord
import time
import _dialog
from datetime import datetime
from botdb.entities.User import User
from botdb.entities.ActivityLog import ActivityLog
from botdb.services import UserService, ActivityLogService
from _newLib import messagesProcessing


# Расчитывает статистику на всех текстовых каналах с указанного времени
async def calc_all_stats_after_time(guild: discord.Guild, time: datetime, spamChannelsId: list) -> str:
    print(guild.name)
    userDict = {}

    for channel in guild.channels:
        if issubclass(type(channel), discord.TextChannel):
            isSpamChannel = True if channel.id in spamChannelsId else False

            async for message in channel.history(limit=10000, oldest_first=False, after=time):
                if message.author.bot:
                    continue

                if message.author.id not in userDict.keys():
                    userDict[message.author.id] = User(userId=message.author.id, messagesCount=0, symbolsCount=0)

                userDict[message.author.id].messagesCount += 1
                textLen = messagesProcessing.text_len(stroke=message.content)
                userDict[message.author.id].symbolsCount += textLen

                if isSpamChannel:
                    ActivityLogService.logOneSpamMessage(guildId=guild.id, userId=message.author.id,
                                                         period= message.created_at.date(), symbolsCount=textLen)
                else:
                    ActivityLogService.logOneMessage(guildId=guild.id, userId=message.author.id,
                                                         period= message.created_at.date(), symbolsCount=textLen)

    answerLog = ['[Поиск сообщений после последней записи на сервере {0}]'.format(guild.name)]

    for keyID in userDict:
        userDict[keyID].exp = (userDict[keyID].symbolsCount + userDict[keyID].messagesCount) / 10

        try:
            UserService.append_stats_on_messages(user=userDict[keyID])

        except Exception:
            answerLog.append(' > новый пользователь:')
            UserService.add_new_user(userId=keyID)
            UserService.append_stats_on_messages(user=userDict[keyID])

        answerLog.append('\t> {0} > сообщений: {1}, символов: {2}'
                         ''.format(keyID, userDict[keyID].messagesCount, userDict[keyID].symbolsCount))

    return '\n'.join(answerLog)


# Возващает статистику пользователя для Embed
def user_stat_embed(ctx, funcX) -> discord.Embed:
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    DBUSer: User = UserService.get_user_by_id(userId=user.id)
    nextLevelExp = funcX(DBUSer.level + 1)
    emb: discord.Embed = discord.Embed(color=discord.colour.Color.dark_magenta(),
                                       title='Пользователь {0}:'.format(user.display_name))
    emb.set_thumbnail(url=user.avatar_url)
    emb.add_field(name='Уровень:', value=str(DBUSer.level))
    emb.add_field(name='Опыт:', value='{0}/{1}'.format(round(DBUSer.exp, 1), nextLevelExp))
    if DBUSer.expModifier != 0:
        fieldName = 'Бонус к опыту:' if DBUSer.expModifier > 0 else 'Штраф к опыту:'
        emb.add_field(name=fieldName, value=str(DBUSer.expModifier))
    emb.add_field(name='Статистика:', value='Отправлено сообщений: {0}\nНапечатано символов: {1}\
    \nВремя в голосовых чатах:{2}'.format(DBUSer.messagesCount, DBUSer.symbolsCount,
                                          time.strftime("%dд::%H:%M:%S", time.gmtime(DBUSer.voiceChatTime)).
                                          replace(' ', '')), inline=False)
    return emb

# Возващает статистику пользователя для Embed
def user_activity_embed(ctx) -> discord.Embed:
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author

    DBActivity: ActivityLog = ActivityLogService.getByPrimaryKey(
        guildId=ctx.guild.id, userId=user.id, period=datetime.now().date())

    emb: discord.Embed = discord.Embed(color=discord.colour.Color.dark_magenta(),
                                       title='Пользователь {0}:'.format(user.display_name))

    emb.set_thumbnail(url=user.avatar_url)

    emb.add_field(name=f'Активность за {datetime.now().date()}:',
                  value=f'Напечатано символов: {DBActivity.symbolsCount}\n'
                        f'Отправленно сообщний: {DBActivity.messagesCount}\n'
                        f'Время в голосовых чатах: {int(DBActivity.voiceChatTime * 10) / 10}c')

    return emb

def seconds_to_str(seconds: int):
    minutes = int(seconds / 60)
    seconds -= minutes * 60

    hours = int(minutes / 60)
    minutes -= hours * 60

    days = int(hours / 24)
    hours -= days * 24

    return f'{days}д:{hours}:{minutes}:{seconds}'



# обновляет статистику из гс
async def voice_stats_update(bot, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState,
                             usersInVoice: dict):
    if before.channel is None:
        usersInVoice[member.id] = time.time()
    if after.channel is None:
        vcTimeCounter = time.time() - usersInVoice.pop(member.id)

        if vcTimeCounter > 10000000:
            await _dialog.message.log(bot=bot, message='{0} - ошибка вычисления времени в гс чате [{1}]'.
                                      format(member.name, vcTimeCounter))
        else:
            UserService.append_stats_on_voice_chat2(userId=member.id, exp=0, voiceChatTime=vcTimeCounter)
            currDate = datetime.now()
            ActivityLogService.logVoiceChatTime(
                guildId=member.guild.id, userId=member.id,
                period=currDate.date(), periodTime=currDate.time(), chatTime=vcTimeCounter)
            await _dialog.message.log(bot=bot, message='{0} пробыл в гс {1}сек.'.format(member.name, vcTimeCounter))
