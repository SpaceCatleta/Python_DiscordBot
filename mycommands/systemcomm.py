from mycommands import dilogcomm
from generallib import textfile as TFile
from configs import config


# Записывает текущие данные в файл
async def writestats(bot, UserStats):
    TFile.WriteSymbolsStat(config.params['SymbolsStatisticsFile'], UserStats)
    await dilogcomm.printlog(bot=bot, message='Статистика записана в файл')
