import datetime


class GuildMember:
    userId: int
    guildId: int
    visitsCount: int

    first_entry_date: datetime.date
    exit_date: datetime.date
    is_present: bool
    ban_functions: bool
    exp: float

    level: int
    messages_count: int
    symbols_count: int
    voice_chat_time: int
    volute_count: int
    exp_modifier: int

    def __init__(self):
        self.userId = 0
        self.guildId = 0
        self.visitsCount = 0

        self.first_entry_date = None
        self.exit_date = None
        self.is_present = False
        self.ban_functions = False
        self.exp = 0

        self.level = 0
        self.messages_count = 0
        self.symbols_count = 0
        self.voice_chat_time = 0
        self.volute_count = 0
        self.exp_modifier = 0


    @staticmethod
    def from_row(row):
        ans = GuildMember()

        ans.userId = row[0]
        ans.guildId = row[1]
        ans.visitsCount = row[2]

        ans.first_entry_date = row[3]
        ans.exit_date = row[4]
        ans.is_present = bool(row[5])
        ans.ban_functions = bool(row[6])
        ans.exp = row[7]

        ans.level = row[8]
        ans.messages_count = row[9]
        ans.symbols_count = row[10]
        ans.voice_chat_time = row[11]
        ans.volute_count = row[12]
        ans.exp_modifier = row[13]

        return ans

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
