
class Gif:
    groupId: int
    gifUrl: str

    def __init__(self, groupId=None, gifUrl=None):
        self.groupId = groupId
        self.gifUrl = gifUrl

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
