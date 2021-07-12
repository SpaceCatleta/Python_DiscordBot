
key_dict = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н',
            'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
            'a':'ф', 's':'ы', 'd':'в', 'f':'а', 'g':'п', 'h':'р', 'j':'о', 'k':'л', 'l':'д', ';':'ж', """'""":'э',
            'z': 'я', 'x':'ч', 'c':'с', 'v':'м', 'b':'и', 'n':'т', 'm':'ь', ',':'б', '.':'ю', '/':'.',
            '{':'х', '}':'ъ', '?': ',', '<':'б', '>':'ю', '`':'ё', '&':'?'}


async def find_and_change_keys(ctx):
    async for message in ctx.channel.history(limit=10, oldest_first=False):
        if message.author.id == ctx.author.id:
            return replace_keyword(message.content)
    return -1


def replace_keyword(text: str) -> str:
    answer = ''
    for symb in text.lower():
        try:
            answer += key_dict[symb]
        except Exception:
            answer += symb
    return answer