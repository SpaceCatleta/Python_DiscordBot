from mycommands import dilogcomm
import TextFile as TFile
import config


# Записывает текущие данные в файл
async def writestats(bot, UserStats):
    TFile.WriteSymbolsStat(config.params['SymbolsStatisticsFile'], UserStats)
    await dilogcomm.sprintlog(bot=bot, message='Статистика записана в файл')
