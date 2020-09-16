from configs import config
from generallib import textfile


# параметры доступа
accessparams = {}


# Читает пользовательские настройки из txt файла
async def init_dictinoraies():
    parlist = textfile.ReadParams(config.params['user_settings'])
    for par in parlist:
        accessparams[par[0]] = par[1]
