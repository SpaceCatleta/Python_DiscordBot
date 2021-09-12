import sqlite3 as sql
from botdb.entities.Question import Question

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_new_question(question: Question):
    cursor.execute("""
        INSERT INTO questions (author_user_id, question_text, answer_text)
        VALUES (:authorUserId, :questionText, :answerText);
        """, question.__dict__)
    connection.commit()


# ====GET============================
def get_question_by_id(questionId: int):
    cursor.execute("""
        SELECT * FROM questions
        WHERE question_id = :questionId;
        """, (questionId,))
    return cursor.fetchone()


def get_question_by_question_text(questionText: str):
    cursor.execute("""
        SELECT * FROM questions
        WHERE question_text = :questionText;
        """, (questionText,))
    return cursor.fetchone()


def search_question_by_question_text(questionText: str):
    cursor.execute("""
        SELECT question_id, author_user_id, question_text
        FROM questions
        WHERE question_text LIKE '%""" + questionText + """%';
        """)
    return cursor.fetchall()


def get_question_uses_count(questionId: int):
    cursor.execute("""
        SELECT question_id, uses_count FROM questions
        WHERE question_id = :questionId;
        """, (questionId,))
    return cursor.fetchone()


def qet_all_questions_texts():
    cursor.execute("""SELECT question_id, question_text FROM questions""")
    return cursor.fetchall()


# ====UPDATE============================
def update_question_answer_text(question: Question):
    cursor.execute("""
        UPDATE questions SET
        answer_text = :answerText
        WHERE question_id = :questionId;
        """, question.__dict__)
    connection.commit()


def update_question_uses_count(question: Question):
    cursor.execute("""
        UPDATE questions SET
        uses_count = :usesCount
        WHERE question_id = :questionId;
        """, question.__dict__)
    connection.commit()


# ====DELETE============================
def delete_question_by_id(questionId: int):
    cursor.execute("""
        DELETE FROM questions
        WHERE question_id = :questionId;
        """, (questionId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM questions; """)
    cursor.execute(""" UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='questions'; """)
    connection.commit()
