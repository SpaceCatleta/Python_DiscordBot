import sqlite3 as sql
from botdb.entities.GeneralSettings import GeneralSettings
from botdb.repository import GeneralSettingsRep as Repos


# ====ADD============================
# Инициализирует настройки со значениями по умолчанию
def create_general_settings():
    Repos.create_general_settings()


# Извлекает настройки из базы данных
def get_general_settings():
    row = Repos.get_general_settings()
    if row is None:
        raise ValueError('GeneralSettingsService.get_general_settings(): returned row is null')
    return GeneralSettings(updateDelay=row[0], timeUntilTimeout=row[1], timeoutsLimit=row[2],
                           bombMessagesTime=row[3], dialogWindowTime=row[4])


# Проверка, инициализированны настройки или нет
def get_general_settings_count():
    return Repos.get_general_settings_count()[0]


# Вовзращает настройки, если их ещё нет, то инициализирует и возвращает их
def get_or_init_general_settings():
    ans = get_general_settings_count()
    if ans == 0:
        create_general_settings()
    return get_general_settings()


# ====UPDATE============================
# Обновляет все поля настроек
def update_general_settings(generalSettings: GeneralSettings):
    Repos.update_general_settings(generalSettings=generalSettings)


# ====DELETE============================
# Удаляет настройки
def delete_general_settings():
    Repos.delete_general_settings()