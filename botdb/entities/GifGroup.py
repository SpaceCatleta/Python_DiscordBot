from datetime import datetime as DateTime


class GifGroup:
    groupId: int
    authorId: int
    createDate: DateTime
    accessLevel: int
    groupType: str
    name: str
    phrase: str

    def __init__(self, groupId=None, authorId=None, createDate=None,
                 accessLevel=None, groupType=None, name=None, phrase=None):
        self.groupId = groupId
        self.authorId = authorId
        self.createDate = createDate
        self.accessLevel = accessLevel
        self.groupType = groupType
        self.name = name
        self.phrase = phrase

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
