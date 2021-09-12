from botdb.entities.Question import Question
from botdb.repository import QuestionRep as Repos

# ====ADD============================
# Добавляет новую запись (необходимы поля author_user_id, question_text, answer_text)
def add_new_question(question: Question):
    Repos.add_new_question(question=question)


# ====GET============================
# Вовзращает все поля вопроса по заданному id
def get_question_by_id(questionId: int):
    row = Repos.get_question_by_id(questionId=questionId)
    if row is None:
        raise ValueError('QuestionService.get_question_by_id(): returned row is null')
    return Question(questionId=row[0], authorUserId=row[1], usesCount=row[2], questionText=row[3], answerText=row[4])


# Вовзращает все поля вопроса по заданному question_text
def get_question_by_question_text(questionText: str):
    row = Repos.get_question_by_question_text(questionText=questionText)
    if row is None:
        raise ValueError('QuestionService.get_question_by_question_text(): returned row is null')
    return Question(questionId=row[0], authorUserId=row[1], usesCount=row[2], questionText=row[3], answerText=row[4])


# Ищет вопросы содержащие указанную подстроку
# Если подстрока найдена - возвращает все поля question, если нет - только question_id, author_user_id, question_text
def search_question_by_question_text(questionText: str):
    rows = Repos.get_question_by_question_text(questionText=questionText)
    if rows is None:
        raise ValueError('QuestionService.search_question_by_question_text(): returned rows is null')
    if len(rows)==1:
        return get_question_by_id(questionId=rows[0])
    print(rows)
    return [Question(questionId=row[0], authorUserId=row[1], questionText=row[2]) for row in rows]


# Возвращает поля question_id и question_test из всех записей
def qet_all_questions_texts():
    rows = Repos.qet_all_questions_texts()
    return [Question(questionId=row[0], questionText=[1]) for row in rows]


# ====UPDATE============================
# Обновляет answer_text вопроса
def update_question_answer_text(question: Question):
    Repos.update_question_answer_text(question=question)


# Прибавляет к счётчику uses_count вопроса указанное число
def append_question_uses_count(questionId: int, addedUsesCount: int):
    row = Repos.get_question_uses_count(questionId=questionId)
    if row is None:
        raise ValueError('QuestionService.append_question_uses_count(): returned row is null')
    Repos.update_question_uses_count(question=Question(questionId=row[0], usesCount=row[1] + addedUsesCount))


# ====DELETE============================
# Цдаляет вопрос с заданным id
def delete_question_by_id(questionId: int):
    Repos.delete_question_by_id(questionId=questionId)


# Удаляет все записи в таблице
def clear_table():
    Repos.clear_table()
