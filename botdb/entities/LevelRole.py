
class LevelRole:
    guildId: int
    level: int
    roleId: int

    def __init__(self, guildId=None, level=None, roleId=None):
        self.guildId = guildId
        self.level = level
        self.roleId = roleId


    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
