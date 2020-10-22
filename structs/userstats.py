from generallib import mainlib


# Поиск по id
def searchid(List: list, ID: int):
    for stat in List:
        if stat.id == ID:
            return stat
    return None


# Описывает статистику одного пользователя
class userstats(object):
    # Уникальный id пользователя
    id: int
    # кол-во опыта
    exp: float
    # уровень
    lvl: int
    # кол-во отправленных сообщений
    mes_counter: int
    # Кол-во напечатанных символов
    symb_counter: int
    # время пребывания в голосовых каналах в секундах
    vc_counter: int
    # Показывает время присоединени к голосовому чату (в хранении статистики не используется)
    connect_time: int
    # Имя пользователя (в харнении статистики не используется)
    name: str

    # Конструктор
    def __init__(self, ID: int, SymbCounter: int = 0, MesCounter: int = 0,
                 VCCounter: int = 0, Exp: float = 0.0, Lvl: int = 0, Name: str = 'NoName'):
        self.id = ID
        self.exp = Exp
        self.lvl = Lvl
        self.mes_counter = MesCounter
        self.symb_counter = SymbCounter
        self.vc_counter = VCCounter
        self.name = Name

    def add(self, addend):
        self.exp += addend.exp
        self.lvl += addend.lvl
        self.mes_counter += addend.mes_counter
        self.symb_counter += addend.symb_counter
        self.vc_counter += addend.vc_counter

    def clear(self, vc_clear: bool = False):
        self.exp = 0
        self.lvl = 0
        self.mes_counter = 0
        self.symb_counter = 0
        if vc_clear:
            self.vc_counter = 0

    # Рассчитывает опыт пользователя
    def calculate_exp(self):
        self.exp = float(round(self.mes_counter / 10 + self.symb_counter / 10, 1))

    def to_string(self):
        return 'name: {0}\nID: {1}\n Exp: {2}\n MesCount {3}\n SymbCount: {4}\n VCTime: {5}s.'.format(self.name,
            self.id, self.exp, self.mes_counter, self.symb_counter, self.vc_counter)
