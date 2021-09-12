import discord
import time
import _dialog
from datetime import datetime
from botdb.entities.User import User
from botdb.services import UserService
from _newLib import messagesProcessing


# Расчитывает статистику на всех текстовых каналах с указанного времени
async def calc_all_stats_after_time(guild: discord.Guild, time: datetime) -> str:
    print(guild.name)
    userDict = {}
    for channel in guild.channels:
        if issubclass(type(channel), discord.TextChannel):
            async for message in channel.history(limit=10000, oldest_first=False, after=time):
                if message.author.bot:
                    continue
                if message.author.id not in userDict.keys():
                    userDict[message.author.id] = User(userId=message.author.id, messagesCount=0, symbolsCount=0)
                userDict[message.author.id].messagesCount += 1
                userDict[message.author.id].symbolsCount += messagesProcessing.text_len(stroke=message.content)

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


# обновляет статистику из гс
async def voice_stats_update(bot, member: discord.Member,  before: discord.VoiceState, after: discord.VoiceState,
                             users_in_vc: dict):
    if before.channel is None:
        users_in_vc[member.id] = time.time()
    if after.channel is None:
        vcTimeCounter = time.time() - users_in_vc.pop(member.id)

        if vcTimeCounter > 10000000:
            await _dialog.message.log(bot=bot, message='{0} - ошибка вычисления времени в гс чате [{1}]'.
                                      format(member.name, vcTimeCounter))
        else:
            UserService.append_stats_on_voice_chat2(userId=member.id, exp=0, voiceChatTime=vcTimeCounter)
            await _dialog.message.log(bot=bot, message='{0} пробыл в гс {1}сек.'.format(member.name, vcTimeCounter))
