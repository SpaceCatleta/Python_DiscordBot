from botdb.entities import GeneralSettings, GifGroup, Gif, LevelRole, User
from botdb.services import GeneralSettingsService, GuildService, UserService, GifGroupService,\
    GifService, SpamChannelsService, ActivityLogService
from botdb.services import LevelRoleService

from _dialog import message
import _dialog
from _newLib import dataProcessing, messagesProcessing, usersProcessing, textFileProcessing, dataBaseProcessing,\
    translateRequest, discordColors
from configs import con_config

from functions import simple as simpleFunctions
import math
import discord.ext.pages
import asyncio
from discord.ext import commands
from dateutil.tz import tzoffset
from datetime import datetime
from botParsers.vk import dataToEmbed
from botParsers.vk import parse as botParsing

# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=con_config.settings['prefix'], intents=intents)

DBGuilds: dict
DBGeneralSettings: GeneralSettings.GeneralSettings
lastWriteTime: str
isSystemWorking: bool = True
usersInVoiceChats = {}


# события при включении бота
@bot.event
async def on_ready():
    dataBaseProcessing.bot = bot
    _dialog.message.bot = bot
    global DBGuilds, DBGeneralSettings, lastWriteTime, usersInVoiceChats
    usersInVoiceChats = {}

    # Подгрузка данных
    with open('configs/ShutdownInfo.txt') as TF:
        lastWriteTime = TF.readline().replace('\n', '')
    DBGeneralSettings = GeneralSettingsService.get_or_init_general_settings()
    DBGuilds = GuildService.get_guild_boot_setup()
    for discordGuild in bot.guilds:
        if discordGuild.id not in DBGuilds.keys():
            GuildService.add_new_guild(guildId=discordGuild.id)
            DBGuilds[discordGuild.id] = GuildService.get_guild_by_guild_id(guildId=discordGuild.id)
            await _dialog.message.log(message='``` [Инициализирован сервер {0}]```'.format(discordGuild.name))

    # дорассчёт статистики
    await _dialog.message.log(message='обнаружено время последней записи: {0}'.format(lastWriteTime))

    try:
        time: datetime = datetime.strptime(lastWriteTime, "%Y-%m-%d %H:%M:%S")
        N = 4
        time.astimezone(tzoffset("UTC+{}".format(N), N * 60 * 60))
        for guildId in DBGuilds:
            discordGuild = bot.get_guild(guildId)
            if discordGuild is None:
                print(f'сервер {guildId} недоступен')
                continue
            answer = await dataProcessing.calc_all_stats_after_time(
                guild=discordGuild, time=time, spamChannelsId=DBGuilds[guildId].spamChannels)
            await _dialog.message.log(message=str(answer))
            await update_counters(bot.get_guild(guildId))

    except ValueError as valErr:
        print('Обработана ошибка:\n' + str(valErr))
        await _dialog.message.log(message=' ошибка при чтении времени, будет только перезаписано время')
        await update_write_time()

    message.generalSettings = DBGeneralSettings
    await _dialog.message.log(message=get_system_check_log(), color='yellow')
    await _dialog.message.log(message='bot online', color='yellow')
    print('booted')
    await update_data_loop()


@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    if mes.content.count('@') > DBGuilds[mes.guild.id].maxLinks:
        await mes.delete()
        await mes.channel.send('```удалено сообщение с недопустимым количеством упоминаний```')
        await _dialog.message.log(message='канал: {0}, пользователь: {1}][удалено сообщение с недопустимым'
                                          'количеством упоминаний'.format(mes.author.name, mes.channel.name))
        return
    count = messagesProcessing.text_len(mes.content)

    if count > 500:
        await _dialog.message.log(author=mes.author, message=mes.content)

    if mes.channel.id in DBGuilds[mes.guild.id].spamChannels:

        ActivityLogService.logOneSpamMessage(
            guildId=mes.guild.id, userId=mes.author.id, period=datetime.now().date(), symbolsCount=count)
        # Пуск команд
        try:
            await asyncio.wait_for(bot.process_commands(message=mes), timeout=DBGeneralSettings.timeUntilTimeout)
        except asyncio.TimeoutError:
            await mes.channel.send('```timeout```')
        return

    # Проверка уровня
    if UserService.append_stats_on_messages_with_level_check(userId=mes.author.id, mesCount=1, symbolsCount=count,
                                                             exp=(count+1)/10, funcX=get_level_from_exp):
        DBUser = UserService.get_user_by_id(userId=mes.author.id)
        DBUser.level = get_level_from_exp(exp=DBUser.exp)
        UserService.update_user(user=DBUser)

        if DBUser.Level in DBGuilds[mes.guild.id].levelsMap.keys():
            await usersProcessing.fix_level_role(user=mes.author, rolesList=mes.guild.roles,
                                                 levelRoleDict=DBGuilds[mes.guild.id].levelsMap,
                                                 funcX=get_level_from_exp,
                                                 exp=DBUser.exp)
        await _dialog.message.bomb_message2(mes=mes, text=f'{mes.author.name} '
                                                          f'получил(а) новый уровень - {DBUser.Level}!', type='error')

    ActivityLogService.logOneMessage(guildId=mes.guild.id, userId=mes.author.id,
                                     period=datetime.now().date(), symbolsCount=count)

    # Пуск команд
    try:
        await asyncio.wait_for(bot.process_commands(message=mes), timeout=DBGeneralSettings.timeUntilTimeout)
    except asyncio.TimeoutError:
        await mes.channel.send('```timeout```')


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await dataProcessing.voice_stats_update(bot=bot, member=member, before=before, after=after,
                                            usersInVoice=usersInVoiceChats)


@bot.event
async def on_member_join(member):
    await _dialog.message.log(message="пользователь {0} зашёл на сервер {1}".
                              format(member.display_name, member.guild.name), color='green')

    if DBGuilds[member.guild.id].welcomePhrase is None:
        embed = discord.Embed(colour=discord.colour.Color.green())
        embed.description = "Пользователь {0} присоединился к нам".format(member.display_name)
        await member.guild.system_channel.send(embed=embed)

    else:
        await member.guild.system_channel.send('{0} {1}'.format(member.mention,
                                                                DBGuilds[member.guild.id].welcomePhrase))

    if DBGuilds[member.guild.id].welcomeGifGroupId is not None:
        triggerGif = GifService.get_random_gif_from_group(DBGuilds[member.guild.id].welcomeGifGroupId)
        await member.guild.system_channel.send(triggerGif.gifUrl)

    await update_counters(member.guild)

    if member.bot:
        return

    try:
        DBUser = UserService.get_user_by_id(userId=member.id)
    except ValueError:
        UserService.add_new_user(userId=member.id)
        DBUser = UserService.get_user_by_id(userId=member.id)

    await usersProcessing.fix_level_role(user=member, rolesList=member.guild.roles,
                                         levelRoleDict=DBGuilds[member.guild.id].levelsMap, funcX=get_level_from_exp,
                                         exp=DBUser.exp)


@bot.event
async def on_member_remove(member):
    await _dialog.message.log(message="пользователь {0} покинул сервер {1}".
                              format(member.display_name, member.guild.name), color='red')
    embed = discord.Embed(colour=discord.colour.Color.red())
    embed.description = "Пользователь {0} покинул нас".format(member.display_name)
    await member.guild.system_channel.send(embed=embed)
    await update_counters(member.guild)


@bot.event
async def on_member_ban(guild, user):
    await _dialog.message.log(message="пользователь {0} был забанен на сервере {1}".
                              format(user.name, guild.name), color='red')
    embed = discord.Embed(colour=discord.colour.Color.red())
    embed.description = "Пользователь {0} был забанен".format(user.name)
    await guild.system_channel.send(embed=embed)


@bot.event
async def on_member_unban(guild, user):
    await _dialog.message.log(message="пользователь {0} был разбанен на сервере {1}".
                              format(user.name, guild.name), color='green')


# ======================================================================================================================
# ПОЛЬЗОВАТЕЛЬСКИЕ КОМАНДЫ
# ======================================================================================================================


@bot.command(name='помощь')
async def users_help(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/users_com_help.txt'))


@bot.command(name='last_update')
async def last_update(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/last_update.txt'))


# Пинг
@bot.command()
async def tm(ctx):
    await ctx.message.delete()
    text = '12 *3* 123'
    await ctx.send(text)


@bot.command()
async def test(ctx):
    await ctx.message.delete()
    text = 'qqq'
    text2 = 'www'
    await _dialog.message.bomb_message2(mes=ctx.message, text=f'{text} '
                                                              f'some text - {text2}!', type='error')


# Переустановка опыта и уровня пользователя
@bot.command()
async def level(ctx, *words):
    await ctx.message.delete()
    await _dialog.message.log(author=ctx.author, message='вызов проверки уровня', ctx=ctx, params=words)

    targetUser = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    print(f'targetUser: {targetUser}')

    DBUser = UserService.get_user_by_id(userId=targetUser.id)
    DBUser.exp = exp_from_stats2(UStats=DBUser)
    DBUser.level = get_level_from_exp(exp=DBUser.exp)
    UserService.update_user(user=DBUser)

    await usersProcessing.fix_level_role(user=targetUser, rolesList=ctx.guild.roles,
                                         levelRoleDict=DBGuilds[ctx.guild.id].levelsMap, funcX=get_level_from_exp,
                                         exp=DBUser.exp)


# Команда транслита с английской раскладки
@bot.command(name='р')
async def change_keyword(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await _dialog.message.log(bot=bot, author=ctx.author, message='вызвал команду -р')
    answer = await simpleFunctions.find_and_change_keys(ctx=ctx)
    if answer == -1:
        await _dialog.message.bomb_message(ctx=ctx, message='сообщение пользователя не найдено среди 10 последних')
    else:
        print(f'display_name: {ctx.author.display_name}')
        await ctx.send(f'{ctx.author.display_name}:\n{answer}')


# Показывает статистику указанного пользователя
@bot.command(name='stats')
async def stats(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    await ctx.send(embed=dataProcessing.user_stat_embed(ctx=ctx, funcX=get_exp_from_level))
    await _dialog.message.log(author=ctx.author, message='вызов статистики', ctx=ctx, params=words)
bot.command(name="stat", pass_context=True)(stats.callback)


# Показывает статистику указанного пользователя
@bot.command(name='daystats')
async def stats(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    await ctx.send(embed=dataProcessing.user_activity_embed(ctx=ctx))
    await _dialog.message.log(author=ctx.author, message='вызов активности за день', ctx=ctx, params=words)


# выводит для печати информацию о глобальных переменных
@bot.command(name='check')
@commands.has_guild_permissions(ban_members=True)
async def stats(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    await ctx.send(f'```{get_system_check_log()}```')
    await _dialog.message.log(author=ctx.author, message='проверка состояния', ctx=ctx, params=words)


# парсит запись VK
@bot.command(name='vk')
async def vk(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    if 'https://vk.com/wall' != words[0][:19]:
        await _dialog.message.bomb_message(ctx=ctx, message='ссылка должна указывать на запись', type='error')
        return
    await ctx.send(embed=dataToEmbed.vk_post_to_embed(botParsing.parse_vk_post(words[0])))
    await _dialog.message.log(author=ctx.author, message='срабатывание парсера', ctx=ctx, params=words)


# Переводит переданный текст на русский (язык определяется автоматически вызываемым сервисом гугла)
@bot.command()
async def translate(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    inputText = ' '.join(words)
    translation = translateRequest.request_googleapis_translate_a(text=inputText)

    embed: discord.Embed = discord.Embed(color=discordColors.magenta)
    embed.add_field(name='исходный текст:', value=inputText, inline=False)
    embed.add_field(name='перевод:', value=translation, inline=False)

    await ctx.send(embed=embed)

bot.command(name="tr", pass_context=True)(translate.callback)


# Команда триггеров
@bot.command()
async def t(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()

    if discord.utils.get(ctx.author.roles, id=DBGuilds[ctx.guild.id].banBotFunctions):
        await _dialog.message.bomb_message(ctx=ctx, message='Данная функция вам недоступна', type='error')
        return

    await _dialog.message.log(author=ctx.author, message='вызов команды триггера', ctx=ctx, params=words)
    """-t [комманда] [ключевое слово] [параметры]"""

    try:
        if words[0] == 'help':      # ===== ПОМОЩЬ
            await ctx.send(textFileProcessing.RadAll(filename='information/triggers_help.txt'))

        elif words[0] == 'list':    # ===== ЗАПРОС ДАННЫХ О ВСЁМ СПИСКЕ
            gifKeyWords = '\t'.join(group.name for group in GifGroupService.get_all_gif_groups())
            await ctx.send(f'```Всего gif: {GifService.get_all_gif_count()}'
                           f'   всего ключевых слов: {GifGroupService.get_gif_group_count()} \n{gifKeyWords}```')

        elif words[0] == 'new':     # ===== ДОБАВЛЕНИЕ НОВОГО КЛЮЧЕВОГО СЛОВА
            if GifGroupService.is_exist_gif_group_by_name(name=words[1]):
                raise ValueError(f'Ключевое слово <{words[1]}> уже занято')
            newGifGroup = GifGroup.GifGroup(name=words[1].lower(), authorId=ctx.author.id,
                                            createDate=datetime.strftime(datetime.now(), "%Y-%m-%d"))
            if len(words) == 2:
                GifGroupService.add_new_gif_group(gifGroup=newGifGroup)
            else:
                newGifGroup.phrase = ' '.join(words[2:])
                GifGroupService.add_new_gif_group_full(gifGroup=newGifGroup)
            await _dialog.message.bomb_message(ctx=ctx, message=f'ключевое слово <{newGifGroup.name}> создано')

        else:                       # ===== ВЫЗОВ GIF
            if words[0] not in ('lock', 'edit', 'rename', 'info', 'add', 'DeleteTrigger', 'delete', 'page'):
                gifGroup = GifGroupService.get_gif_group_by_name(name=words[0])
                if len(ctx.message.mentions) > 0:
                    text = f'{ctx.author.mention} {gifGroup.phrase} {ctx.message.mentions[0].mention}'\
                        if gifGroup.phrase is not None else ctx.message.mentions[0].mention
                    await ctx.send(text + '\n' + GifService.get_random_gif_from_group(groupId=gifGroup.groupId).gifUrl)
                else:
                    if len(words) >= 2 and words[1].isdigit():
                        randomGif = GifService.get_gif(groupId=gifGroup.groupId, index=int(words[1]))
                    else:
                        randomGif = GifService.get_random_gif_from_group(groupId=gifGroup.groupId)
                    await ctx.send(randomGif.gifUrl)
                return

            gifGroup = GifGroupService.get_gif_group_by_name(name=words[1])

            if words[0] == 'info':    # ===== ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ТРИГГЕРЕ
                count = GifService.get_gif_count_by_group_id(groupId=gifGroup.groupId)
                answer = await dataBaseProcessing.print_gif_group(gifGroup=gifGroup, gifCount=count)
                await ctx.send(f'```{answer}```')
                return

            if not (gifGroup.authorId == ctx.author.id or gifGroup.accessLevel == 1
                    or ctx.author.guild_permissions.administrator):
                raise ValueError('у вас нет прав использовать данную команду')

            if words[0] == 'lock':      # ===== СМЕНА РЕЖИМА ДОСТУПА
                gifGroup.accessLevel = int(not gifGroup.accessLevel)
                GifGroupService.update_gif_group_access_level(gifGroup=gifGroup)

            elif words[0] == 'edit':    # ===== СМЕНА ФРАЗЫ ТРИГГЕРА
                gifGroup.phrase = ' '.join(words[2:])
                GifGroupService.update_gif_group_phrase(gifGroup=gifGroup)
                await _dialog.message.bomb_message(ctx=ctx, message='фраза изменена')

            elif words[0] == 'rename':  # ===== ПЕРЕИМЕНОВЫВАЕНИЕ ГРУППЫ
                newName = words[2].lower()
                gifGroup.name = newName
                GifGroupService.update_gif_group(gifGroup=gifGroup)
                await _dialog.message.bomb_message(ctx=ctx, message='ключевое слово изменено')

            elif words[0] == 'add':     # ===== ДОБАВЛЕНИЕ GIF
                gifUrl = await search_gif_mes(ctx=ctx)
                GifService.add_new_gif(gif=Gif.Gif(groupId=gifGroup.groupId, gifUrl=gifUrl))
                await _dialog.message.bomb_message(ctx=ctx, message=f'добавлено в <{gifGroup.name}>')

            elif words[0] == 'page':    # ===== ВЫВОД 10 GIF
                if not words[2].isdigit():
                    raise ValueError('число введено неверно')
                for gifData in GifService.get_gif_page(groupId=gifGroup.groupId, index=int(words[2])):
                    await ctx.send(gifData.gifUrl)

            elif words[0] == 'DeleteTrigger':   # ===== УДАЛЕНИЕ ГРУППЫ
                GifService.delete_all_gif_by_group_id(groupId=gifGroup.groupId)
                GifGroupService.delete_gif_group_by_id(groupId=gifGroup.groupId)
                await _dialog.message.bomb_message(ctx=ctx,
                                                   message=f'Ключевое слово <{gifGroup.name}> удалено')

            elif words[0] == 'delete':          # ===== УДАЛЕНИЕ GIF
                if not words[2].isdigit():
                    raise ValueError('число введено неверно')
                GifService.delete_gif_by_group_id_and_index(groupId=gifGroup.groupId, index=int(words[2]))
                await _dialog.message.bomb_message(ctx=ctx, message=f'gif удалена из <{gifGroup.name}>')

    except ValueError as valErr:
        await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')

bot.command(name="т", pass_context=True)(t.callback)


# Поиск gif (дял команды выше)
async def search_gif_mes(ctx):
    async for curMessage in ctx.channel.history(limit=10, oldest_first=False):
        if curMessage.content[0:8] == 'https://':
            await curMessage.delete()
            return curMessage.content
    raise ValueError('в последних 10 сообщениях gif не обнаружены')


# ======================================================================================================================
# ГРУППА КОМАНД МОДЕРАЦИИ
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='mod')
@commands.has_guild_permissions(manage_channels=True)
async def mod(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await _dialog.message.log(author=ctx.author, message='Воспользовался модераторской командой',
                              params=ctx.message.content.split(' '))


@mod.command(name='help')
async def show(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/moder_com_help.txt'))


# Удаление сообщений
@mod.command(name='clearmes')
async def clear_messages(ctx: discord.ext.commands.Context, *words):

    try:
        if not words[0].isdigit():
            raise ValueError('число введено неверно')

        messagesToDelete = int(words[0])
        discordUser = messagesProcessing.get_user_link_no_exception(ctx=ctx)
        isDeleteExp = False

        if len(words) > 1:
            if words[1] == '-exp':
                isDeleteExp = True

        print(f'messagesToDelete: {messagesToDelete}')
        print(f'discordUser: {discordUser}')
        print(f'isDeleteExp: {isDeleteExp}')

        await messagesProcessing.delete_messages(bot, ctx=ctx, n=messagesToDelete,
                                                 discordUser=discordUser, isDeleteExp=isDeleteExp)

    except ValueError as valErr:
        await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')


# выдаёт бонус/штраф к опыту
@mod.command()
async def exp(ctx: discord.ext.commands.Context, *words):
    try:
        if not (words[0].isdigit() or words[0][1:].isdigit()):
            raise ValueError('число введено неверно')
        expChanging = int(words[0])

        discordUser = messagesProcessing.get_user_link(ctx=ctx)
        UserService.add_user_exp_modifier2(userId=discordUser.id, exp=expChanging, expModifier=expChanging)
        # Это вставка из -level для уточнения уровня
        DBUser = UserService.get_user_by_id(userId=discordUser.id)
        DBUser.exp = exp_from_stats2(UStats=DBUser)
        DBUser.level = get_level_from_exp(exp=DBUser.exp)
        UserService.update_user(user=DBUser)

        text = 'бонус к опыту выдан' if expChanging >= 0 else 'штраф к опыту выдан'
        await _dialog.message.bomb_message(ctx=ctx, message=text)
    except ValueError as valErr:
        await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')


# мутит команды бота
@mod.command()
async def ban(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        role = discord.utils.get(iterable=ctx.guild.roles, id=DBGuilds[ctx.guild.id].banBotFunctions)
        if role is None:
            await _dialog.message.bomb_message(ctx=ctx, message='роль сохранённая в настроках не найдена', type='error')
            return
        await ctx.send(f'```Пользователю {ctx.message.mentions[0].name} '
                       f'ограничены функции на {DBGuilds[ctx.guild.id].muteTime}с.```')
        await usersProcessing.give_timer_role(user=ctx.message.mentions[0], role=role,
                                              timeSeconds=DBGuilds[ctx.guild.id].muteTime)
    else:
        raise ValueError('Не указан пользователь')


# мутит команды бота
@mod.command()
async def light_mute(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        role = discord.utils.get(iterable=ctx.guild.roles, id=DBGuilds[ctx.guild.id].lightMuteRoleId)
        if role is None:
            await _dialog.message.bomb_message(ctx=ctx, message='роль сохранённая в настроках не найдена', type='error')
            return
        await ctx.send(f'```Пользователь {ctx.message.mentions[0].name} '
                       f'ограничен в текстовых каналах на {DBGuilds[ctx.guild.id].muteTime}с.```')
        await usersProcessing.give_timer_role(user=ctx.message.mentions[0], role=role,
                                              timeSeconds=DBGuilds[ctx.guild.id].muteTime)
    else:
        raise ValueError('Не указан пользователь')


# мутит указанного пользователя
@mod.command()
async def mute(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        role = discord.utils.get(iterable=ctx.guild.roles, id=DBGuilds[ctx.guild.id].muteRoleId)
        if role is None:
            await _dialog.message.bomb_message(ctx=ctx, message='роль сохранённая в настроках не найдена', type='error')
            return

        words = ctx.message.content.split(' ')
        muteTime = DBGuilds[ctx.guild.id].muteTime
        if len(words) >= 4:
            try:
                muteTime = messagesProcessing.get_time(text=ctx.message.content.split(' ')[2])
            except ValueError as valErr:
                await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')

        await ctx.send(f'```Пользователю {ctx.message.mentions[0].name} '
                       f'выдан мут на {DBGuilds[ctx.guild.id].muteTime}с.```')
        await usersProcessing.give_timer_role(user=ctx.message.mentions[0], role=role,
                                              timeSeconds=muteTime)
    else:
        raise ValueError('Не указан пользователь')


# мутит указанного пользователя
@mod.command()
async def voice_mute(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        role = discord.utils.get(iterable=ctx.guild.roles, id=DBGuilds[ctx.guild.id].muteVoiceChatRoleId)
        if role is None:
            await _dialog.message.bomb_message(ctx=ctx, message='роль сохранённая в настроках не найдена', type='error')
            return
        await ctx.send(f'```Пользователю {ctx.message.mentions[0].name} '
                       f'ограничен доступ к голосовым каналам {DBGuilds[ctx.guild.id].muteTime}с.```')
        await usersProcessing.give_timer_role(user=ctx.message.mentions[0], role=role,
                                              timeSeconds=DBGuilds[ctx.guild.id].muteTime)
    else:
        raise ValueError('Не указан пользователь')


# ======================================================================================================================
# ГРУППА СЕРВЕРНЫХ КОМАНД
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='guild')
@commands.has_guild_permissions(ban_members=True)
async def guild(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await _dialog.message.log(author=ctx.author, message='Воспользовался командой настроек сервера',
                              params=ctx.message.content.split(' '))


@guild.command(name='help')
async def guild_help(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/guild_com_help.txt'))


# Выводит все настройки сервера
@guild.command(name='show')
async def show(ctx: discord.ext.commands.Context):
    await ctx.send(content=f'```{DBGuilds[ctx.guild.id]}```')


# Выводит все настройки сервера
@guild.command(name='spam')
async def spam(ctx: discord.ext.commands.Context):
    guildId = ctx.guild.id
    channelId = ctx.channel.id

    if SpamChannelsService.is_exist(guildId=guildId, channelId=channelId):
        SpamChannelsService.delete_by_id(guildId=guildId, channelId=channelId)
        DBGuilds[guildId].spamChannels.remove(channelId)

        await _dialog.message.log(author=ctx.author, message='Удалил канал из списка спама')
        await _dialog.message.bomb_message(ctx=ctx, message='Канал удалён из списка спама')
    else:
        SpamChannelsService.add2(guildId=guildId, channelId=channelId)
        DBGuilds[guildId].spamChannels.append(channelId)

        await _dialog.message.log(author=ctx.author, message='Добавил канал в список спама')
        await _dialog.message.bomb_message(ctx=ctx, message='Канал добавлен в список спама')


# Изменение настройки сервера
@guild.command(name='set')
async def set_param(ctx: discord.ext.commands.Context, *words):
    try:
        if words[0] not in DBGuilds[ctx.guild.id].__dict__.keys():
            await message.bomb_message(ctx=ctx, message='Неверное ключевое слово', type='error')
        else:
            if words[0] in ('maxLinks', 'muteTime', 'personalRolesAllowed'):
                DBGuilds[ctx.guild.id].__dict__[words[0]] = int(words[1])
                GuildService.update_guild_common(guild=DBGuilds[ctx.guild.id])

            elif words[0] in ('banBotFunctions', 'noLinksRoleId',
                              'lightMuteRoleId', 'muteRoleId', 'muteVoiceChatRoleId'):
                roleId = messagesProcessing.get_role(ctx=ctx, bufferParts=3).id
                DBGuilds[ctx.guild.id].__dict__[words[0]] = roleId
                GuildService.update_guild_roles(guild=DBGuilds[ctx.guild.id])

            elif words[0] == 'welcomePhrase':
                DBGuilds[ctx.guild.id].__dict__[words[0]] = ' '.join(words[1:])
                GuildService.update_guild_welcome_phrase(guild=DBGuilds[ctx.guild.id])

            elif words[0] == 'welcomeGifGroupId':
                gifGroup: GifGroup.GifGroup = GifGroupService.get_gif_group_by_name(name=words[1])
                DBGuilds[ctx.guild.id].__dict__[words[0]] = gifGroup.groupId
                GuildService.update_welcome_gif_group_id(guild=DBGuilds[ctx.guild.id])

            elif words[0] == 'membersCounterChatId':
                DBGuilds[ctx.guild.id].__dict__[words[0]] = messagesProcessing.get_text_chat_link(ctx=ctx).id
                GuildService.update_guild_chats(guild=DBGuilds[ctx.guild.id])

            else:
                await message.bomb_message(ctx=ctx, message='Данная настройка в данное время недоступна ', type='error')
                return
            await message.bomb_message(ctx=ctx, message=f'Настройка {words[0]} обновлена')

    except ValueError as valErr:
        await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')


# Изменение настройки сервера
@guild.command(name='level')
async def edit_level(ctx: discord.ext.commands.Context, *words):
    global DBGuilds
    guildId = ctx.guild.id
    "-guild level | set {level} {roleId}"""

    try:
        if not words[1].isdigit():
            raise ValueError('Уровень введён неверно')

        levelNum = int(words[1])

        if words[0] == 'set':
            roleId = messagesProcessing.get_role(ctx=ctx, bufferParts=4).id
            levelRole = LevelRole.LevelRole(guildId=guildId, level=levelNum, roleId=roleId)

            if levelNum in DBGuilds[guildId].levelsMap.keys():
                LevelRoleService.update_level_role(levelRole=levelRole)
            else:
                LevelRoleService.add_level_role(levelRole=levelRole)

            DBGuilds[guildId].levelsMap[levelNum] = roleId
            await _dialog.message.bomb_message(ctx=ctx, message='роль установлена')

        elif words[0] == 'delete':
            LevelRoleService.delete_level_role_by_guild_id_and_level(guildId=guildId, level=levelNum)
            if levelNum in DBGuilds[guildId].levelsMap.keys():
                DBGuilds[guildId].levelsMap.pop(levelNum)
            await _dialog.message.bomb_message(ctx=ctx, message='роль удалена')

    except ValueError as valErr:
        await _dialog.message.bomb_message(ctx=ctx, message=str(valErr), type='error')


# Изменение настройки сервера
@guild.command(name='update_levels')
async def update_levels(ctx: discord.ext.commands.Context):
    global DBGuilds

    i = 0
    for discordUser in ctx.guild.members:
        if discordUser.bot:
            continue
        try:
            DBUser = UserService.get_user_by_id(userId=discordUser.id)
        except ValueError:
            UserService.add_new_user(userId=discordUser.id)
            await _dialog.message.log(message=f'[{ctx.guild.name}] Обнаружен пользователь {discordUser.name} ',
                                      color='yellow')
            DBUser = UserService.get_user_by_id(userId=discordUser.id)
        oldLevel = DBUser.level
        DBUser.level = get_level_from_exp(exp=DBUser.exp)
        newLevel = DBUser.level
        if oldLevel < newLevel:
            i += 1
        UserService.update_user(user=DBUser)
        await usersProcessing.fix_level_role(user=discordUser, rolesList=ctx.guild.roles,
                                             levelRoleDict=DBGuilds[ctx.guild.id].levelsMap, funcX=get_level_from_exp,
                                             exp=DBUser.exp)

    await _dialog.message.bomb_message(ctx=ctx, message=f'обновлено пользователей {i}')


# ======================================================================================================================
# ГРУППА КОММАНД СТАТИСТИКИ АКТИВНОСТИ
# ======================================================================================================================


# Общая функция группы
@bot.group(name='activity')
@commands.has_guild_permissions(manage_channels=True)
async def activity(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await _dialog.message.log(author=ctx.author, message='Воспользовался командой статистики',
                              params=ctx.message.content.split(' '))


@activity.command(name='help')
async def activity_help(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/activity_com_help.txt'))


@activity.command(name='afk')
async def activity_afk(ctx: discord.ext.commands.Context, *words):
    daysToCheck, outLen = 0, 10
    try:
        daysToCheck = int(words[0])
        outLen = int(words[1]) if len(words) > 1 else 10
    except ValueError:
        await _dialog.message.bomb_message(ctx=ctx, message='неверный ввод', type='error')

    members_list = tuple(filter(lambda val: not val.bot, ctx.guild.members))
    members_dict = {val.id: val for val in members_list}

    idList = ActivityLogService.get_afk_users_id_after_date(
        guild_id=ctx.guild.id, daysToCheck=daysToCheck,
        guildMembersIdList=tuple(val.id for val in members_list))

    size = len(idList)
    outLen = outLen if outLen <= size else size
    idList = idList[:outLen]
    # text = '\n'.join(map(str, idList))
    text = '\n'.join(tuple(members_dict[val].mention for val in idList))
    await ctx.send(f'За последние {daysToCheck} дней\n'
                   f'Найдено неактивных пользователей : {size}\n'
                   f'id {outLen} неактивных:\n{text}')


# ======================================================================================================================
# ГРУППА СИСТЕМНЫХ КОММАНД
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='sys')
@commands.has_guild_permissions(ban_members=True)
async def sys(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await _dialog.message.log(author=ctx.author, message='Воспользовался системной командой',
                              params=ctx.message.content.split(' '))


@sys.command(name='help')
async def sys_help(ctx: discord.ext.commands.Context):
    await ctx.send(textFileProcessing.RadAll(filename='information/system_com_help.txt'))


# Выводит все сервера, где подключён бот
@sys.command(name='guilds')
async def guilds(ctx: discord.ext.commands.Context):
    await ctx.send('```{0}```'.format('\n'.join([discordGuild.name for discordGuild in bot.guilds])))


# Выводит все настройки системы
@sys.command(name='show')
async def show(ctx: discord.ext.commands.Context):
    await ctx.send(content=f'```{DBGeneralSettings}```')


# Изменение общих настроек
@sys.command(name='set')
async def set_param(ctx: discord.ext.commands.Context, *words):
    if words[0] not in DBGeneralSettings.__dict__.keys():
        await message.bomb_message(ctx=ctx, message='Неверное ключевое слово', type='error')
    else:
        DBGeneralSettings.__dict__[words[0]] = int(words[1])
        GeneralSettingsService.update_general_settings(generalSettings=DBGeneralSettings)
        await message.bomb_message(ctx=ctx, message=f'Настройка {words[0]} обновлена')


# команда завершения работы
@sys.command(name='off')
async def sys_shutdown():
    global isSystemWorking
    await update_write_time()
    await _dialog.message.log(bot=bot, message='bot offline')
    isSystemWorking = False
    await bot.close()


# ======================================================================================================================
# СИСТЕМНЫЕ ФУНКЦИИ
# ======================================================================================================================


def get_exp_from_level(exp: float):
    return 500 + (exp - 1) * 2000 * (exp / 10)


def get_level_from_exp(exp: float):
    return 0 if exp < 450 else int(0.5 + math.sqrt(exp - 450) / (10 * (math.sqrt(2))))


def exp_from_stats(symbols: int, messages: int, time: int, expMod: float):
    return (symbols + messages) / 10.0 + time * 0 + expMod
    # + round(time / 60, 1)


def exp_from_stats2(UStats: User.User):
    return exp_from_stats(symbols=UStats.symbolsCount, messages=UStats.messagesCount,
                          time=UStats.voiceChatTime, expMod=UStats.expModifier)


async def update_counters(discordGuild):
    if DBGuilds[discordGuild.id].membersCounterChatId is None:
        return
    memberCounterChannel = discord.utils.get(discordGuild.text_channels,
                                             id=DBGuilds[discordGuild.id].membersCounterChatId)
    await memberCounterChannel.edit(name=f'Участников: {discordGuild.member_count}')


async def update_data_loop():
    while isSystemWorking:
        await update_write_time()
        await asyncio.sleep(DBGeneralSettings.updateDelay)


# обновляет время последней записи
async def update_write_time():
    global lastWriteTime
    lastWriteTime = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    with open('configs/ShutdownInfo.txt', 'w') as TF:
        TF.write(lastWriteTime)


# выводит для печати информацию о глобальных переменных
def get_system_check_log():
    answer = f'guilds: {"none" if DBGuilds is None else len(DBGuilds.keys())}\n'
    answer += f'general settings: {"none" if DBGeneralSettings is None else "loaded"}\n'
    answer += f'last write time: {lastWriteTime}\n'
    answer += f'users in voice chats: {"null" if usersInVoiceChats is None else len(usersInVoiceChats.keys())}'
    return answer


if __name__ == '__main__':
    print('boot')
    bot.run(con_config.settings['token'])
