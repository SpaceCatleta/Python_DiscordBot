import discord
import asyncio
from generallib import mainlib

# список базовых реакций для вариантов выборов
base_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
# Словарь для перевода реакции в номер варианта
emoji_dict = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9, '🔟': 10}


# Создаёт голосование
def create_vote(bot, ctx: discord.ext.commands.Context):
    input_args: list = ctx.message.content.split(' ')
    input_args.pop(0)
    timer = input_args.pop(0)
    title = input_args.pop(0)
    l_args = []
    for arg in input_args:
        l_args.append(arg)
    return Vote(bot=bot, ctx=ctx, title=title, timer=int(timer), choises=l_args)

# Описывает один вариант выбора в голосовании
class VoteChoise(object):
    # Текст выбора
    text: str
    # Голоса за данный вариант
    votes: int

    # Конструктор
    def __init__(self, Text: str):
        self.text = Text
        self.votes = 0


# Описывает голосование в дискорде
class Vote(object):
    # тело бота
    bot = None
    # Тема голосования
    vote_title: str
    # контекст
    context: discord.ext.commands.Context
    # ембед
    embed = discord.Embed
    # количество вариантов выбора
    choises_count: int
    # варианы выбора и голоса за них
    vote_choises: list = []
    # голоса (реакции) и пользователи, что их отправили
    votes: list = []
    # время на вборы (таймер)
    exist_time: int
    # проголосовавшие пользователи
    voted_users = []

    # коструктор
    def __init__(self, bot, ctx, title: str, timer, choises: list):
        self.bot = bot
        self.context = ctx
        self.embed = discord.Embed(colour=discord.colour.Color.dark_magenta())
        self.embed.title = title
        self.vote_title = title
        self.exist_time = timer
        self.embed.description = ''
        self.votes = []
        self.voted_users = []
        self.vote_choises = []

        i = 0
        for choise in choises:
            i += 1
            self.embed.description += '{0}) {1}\n'.format(i, choise)
            self.vote_choises.append(VoteChoise(Text=choise))

        self.embed.description += 'Время голосования: {}сек.'.format(self.exist_time)
        self.choises_count = len(choises)

    # Выводит голосование в чат
    async def show(self):
        mes: discord.Message = await self.context.send(embed=self.embed)
        i = 0
        while i < self.choises_count:
            await mes.add_reaction(emoji=base_emoji[i])
            i += 1

        await asyncio.sleep(self.exist_time)

        answer = ''
        self.CalculateVotes()
        for choise in self.vote_choises:
            answer += '{0}  --  {1} голосов\n'.format(choise.text, choise.votes)

        descr_text = '{0}\nБыло сделано {1} голосов\n\n'.format(self.vote_title, len(self.voted_users)) + answer
        await self.context.send(embed=discord.Embed(title='Итоги голосования', description=descr_text))
        await mes.delete()

    # Добавление голоса
    def add_vote(self, emoji, user):
        if user.bot is True:
            return
        try:
            self.votes.append([user.id, emoji_dict[str(emoji)]])
        except Exception:
            pass

    # Подсчёт голосов
    def CalculateVotes(self):
        for item in self.votes:
            if mainlib.is_match(el_list=self.voted_users, value=item[0]):
                continue
            else:
                self.voted_users.append(item[0])
                self.vote_choises[item[1]-1].votes += 1
