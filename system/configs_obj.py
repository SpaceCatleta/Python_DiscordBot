import csv


# хранит системные настройки и обеспечивает работу с файлом настроек
class GeneralConfig(object):
    _file_path: str = 'system\general_configs.csv'
    _dict = {}
    # период обновления вреемени записи
    _time_update_delay = 60
    # максимальное кол-во линков
    _max_links = 0
    # таймаут выполнения функции
    _timeout = 60
    # количество аймаутов, до сброса комманд
    _timeout_limit = 3
    # время существования системного сообщения
    _bomb_mes_time = 10


# ========================== СВОЙСТВА ==============================


    # свойство - период обновления
    @property
    def time_update_delay(self):
        return self._time_update_delay

    @time_update_delay.setter
    def time_update_delay(self, value: int):
        self._time_update_delay = value
        self._dict['time_update_delay'] = str(value)
        self._rewrite_csv()

    # свойство - максимальное кол-во линков
    @property
    def max_links(self):
        return self._max_links

    @max_links.setter
    def max_links(self, value: int):
        self._max_links = value
        self._dict['max_links'] = str(value)
        self._rewrite_csv()

    # свойство - таймаут выполнения функции
    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value
        self._dict['timeout'] = str(value)
        self._rewrite_csv()

    # свойство - количество аймаутов, до сброса комманд
    @property
    def timeout_limit(self):
        return self._timeout_limit

    @timeout_limit.setter
    def timeout_limit(self, value: int):
        self._timeout_limit = value
        self._dict['timeout_limit'] = str(value)
        self._rewrite_csv()

    # свойство - время существования системного сообщения
    @property
    def bomb_mes_time(self):
        return self._bomb_mes_time

    @bomb_mes_time.setter
    def bomb_mes_time(self, value: int):
        self._bomb_mes_time = value
        self._dict['bomb_mes_time'] = str(value)
        self._rewrite_csv()


# ========================== МЕТОДЫ ==============================


    def __init__(self):
        with open(self._file_path, newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self._dict = row
        self._max_links = int(self._dict['max_links'])
        self._time_update_delay = int(self._dict['time_update_delay'])
        self._timeout = int(self._dict['timeout'])
        self._timeout_limit = int(self._dict['timeout_limit'])

    # Устанавливает значение по ключу
    def set_by_key(self, key: str, value: int):
        if key == 'max_links': self.max_links = value
        elif key == 'time_update_delay': self.time_update_delay = value
        elif key == 'timeout': self.timeout = value
        elif key == 'timeout_limit': self.timeout_limit = value
        elif key == 'bomb_mes_time': self.bomb_mes_time = value
        else: return -1
        return 0

    # Перезаписывает csv файл
    def _rewrite_csv(self):
        with open(self._file_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=[*self._dict])
            writer.writeheader()
            writer.writerow(self._dict)

    def print(self) -> str:
        return '\n'.join(['{0} = {1}'.format(key, self._dict[key]) for key in [*self._dict]])


# Объект-контейнер настроек ролей
class RolesConfig(object):
    _file_path: str = 'system\servroles_configs.csv'
    _dict = {}
    _base_role = 'None'
    _ban_functions = 'None'
    _moot = 'None'
    _vc_moot = 'None'

    @property
    def base_role(self):
        return self._base_role

    @base_role.setter
    def base_role(self, value: str):
        self._base_role = value
        self._dict['base_role'] = str(value)
        self._rewrite_csv()

    @property
    def ban_functions(self):
        return self._ban_functions

    @ban_functions.setter
    def ban_functions(self, value: str):
        self._ban_functions = value
        self._dict['ban_functions'] = str(value)
        self._rewrite_csv()

    @property
    def moot(self):
        return self._moot

    @moot.setter
    def moot(self, value: str):
        self._moot = value
        self._dict['moot'] = str(value)
        self._rewrite_csv()

    @property
    def vc_moot(self):
        return self._vc_moot

    @vc_moot.setter
    def vc_moot(self, value: str):
        self._vc_moot = value
        self._dict['vc_moot'] = str(value)
        self._rewrite_csv()

    def __init__(self):
        with open(self._file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self._dict = row
        self._base_role = self._dict['base_role']
        self._ban_functions = self._dict['ban_functions']
        self._moot = self._dict['moot']
        self._vc_moot = self._dict['vc_moot']

    def set_by_key(self, key: str, value: str):
        if key == 'base_role': self.base_role = value
        elif key == 'ban_functions': self.ban_functions = value
        elif key == 'moot':  self.moot = value
        elif key == 'vc_moot': self.vc_moot = value
        else: return -1
        return 0

    def _rewrite_csv(self):
        with open(self._file_path, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[*self._dict])
            writer.writeheader()
            writer.writerow(self._dict)

    def print(self) -> str:
        return '\n'.join(['{0} = {1}'.format(key, self._dict[key]) for key in [*self._dict]])
