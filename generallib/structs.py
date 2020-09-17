# Поиск по id
def searchid(list, ID: int):
    for stat in list:
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
                 VCCounter: int = 0, Exp: float = 0.0, Lvl: int = 0):
        self.id = ID
        self.exp = Exp
        self.lvl = Lvl
        self.mes_counter = MesCounter
        self.symb_counter = SymbCounter
        self.vc_counter = VCCounter
