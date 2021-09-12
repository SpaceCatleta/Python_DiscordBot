
class Question:
    questionId: int
    authorUserId: int
    usesCount: int
    questionText: str
    answerText: str

    def __init__(self, questionId=None, authorUserId=None, usesCount=None, questionText=None, answerText=None):
        self.questionId = questionId
        self.authorUserId = authorUserId
        self.usesCount = usesCount
        self.questionText = questionText
        self.answerText = answerText

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
