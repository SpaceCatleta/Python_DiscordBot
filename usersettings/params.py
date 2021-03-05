from configs import config
from generallib import textfile

# параметры доступа
shutdownparams = {}

# Читает пользовательские настройки из txt файла
async def init_dictinoraies():
    par_list = textfile.ReadParams(config.params['shutdown_info'], delsymb='=')
    for par in par_list:
        shutdownparams[par[0]] = par[1]
