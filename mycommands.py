# Команда отключения бота
def shutdown(ctx):
    ctx.send('bot was turned off')
    exit()


# Тестовое приветствие
async def hello(ctx):
    # Объявляем переменную author и записываем туда информацию об авторе.
    author = ctx.message.author

    # Выводим сообщение с упоминанием автора, обращаясь к переменной author.
    # await ctx.send(f'Hello, {author.mention}!')
    await ctx.send(f'101')

