
class GeneralSettings:
    updateDelay: int
    timeUntilTimeout: int
    timeoutsLimit: int
    bombMessagesTime: int
    dialogWindowTime: int

    def __init__(self, updateDelay=None, timeUntilTimeout=None, timeoutsLimit=None,
                 bombMessagesTime=None, dialogWindowTime=None):
        self.updateDelay = updateDelay
        self.timeUntilTimeout = timeUntilTimeout
        self.timeoutsLimit = timeoutsLimit
        self.bombMessagesTime = bombMessagesTime
        self.dialogWindowTime = dialogWindowTime

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
