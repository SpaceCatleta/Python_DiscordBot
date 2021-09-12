import unittest
from botdb.services import UserService
from botdb.services import QuestionService
from botdb.entities.Question import Question


class TestQuestionServiceService(unittest.TestCase):

    def _check_data(self, checking_obj: Question, control_obj: Question):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    @classmethod
    def setUpClass(cls):
        QuestionService.clear_table()
        UserService.clear_table()

        UserService.add_new_user(userId=11)
        UserService.add_new_user(userId=12)

        print('\n[[[   TESTING QuestionService  ]]]\n')

    def setUp(self):
        QuestionService.clear_table()
        QuestionService.add_new_question(question=Question(authorUserId=11, questionText='вопр1', answerText='ответ1'))
        QuestionService.add_new_question(question=Question(authorUserId=12, questionText='вопр2', answerText='ответ2'))

    # =====================
    def test_add_question_and_get_question_by_id(self):
        print('Testing add_question() and get_question_by_id()')
        question = Question(questionId=3, authorUserId=11, usesCount=0, questionText='вопр3', answerText='ответ3')

        QuestionService.add_new_question(question=question)
        answer = QuestionService.get_question_by_id(questionId=3)

        self._check_data(checking_obj=answer, control_obj=question)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_question_by_question_text(self):
        print('Testing get_question_by_question_text()')

        answer = QuestionService.get_question_by_question_text(questionText='вопр1')
        check_obj = Question(questionId=1, authorUserId=11, usesCount=0, questionText='вопр1', answerText='ответ1')

        self._check_data(checking_obj=answer, control_obj=check_obj)
        print('Successful\n')
    # =====================

    # =====================
    # def test_search_question_by_question_text(self):
    #     print('Testing search_question_by_question_text()')
    #     print('Test 1')
    #
    #     answer = QuestionService.search_question_by_question_text(questionText='вопр')
    #
    #     self.assertEqual(len(answer), 2, 'rows count should be {0} actual {1}'.format(2, len(answer)))
    #
    #     print('Test 2')
    #     answer = QuestionService.search_question_by_question_text(questionText='вопр1')
    #
    #     check_obj = Question(questionId=1, authorUserId=11, usesCount=0, questionText='вопр1', answerText='ответ1')
    #     self._check_data(checking_obj=answer, control_obj=check_obj)
    #     print('Successful\n')
    # =====================

    # =====================
    def test_qet_all_questions_texts(self):
        print('Testing qet_all_questions_texts()')

        answer = QuestionService.qet_all_questions_texts()

        self.assertEqual(len(answer), 2, 'rows count should be {0} actual {1}'.format(2, len(answer)))
        print('Successful\n')
    # =====================

    # =====================
    def test_update_question_answer_text(self):
        print('Testing update_question_answer_text()')
        question = Question(questionId=1, authorUserId=11, usesCount=0, questionText='вопр1', answerText='ответ111')

        QuestionService.update_question_answer_text(question=question)
        answer = QuestionService.get_question_by_id(questionId=1)

        self._check_data(checking_obj=answer, control_obj=question)
        print('Successful\n')
    # =====================

    # =====================
    def test_append_question_uses_count(self):
        print('Testing append_question_uses_count()')
        question = Question(questionId=1, authorUserId=11, usesCount=5, questionText='вопр1', answerText='ответ1')

        QuestionService.append_question_uses_count(questionId=1, addedUsesCount=2)
        QuestionService.append_question_uses_count(questionId=1, addedUsesCount=3)
        answer = QuestionService.get_question_by_id(questionId=1)

        self._check_data(checking_obj=answer, control_obj=question)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_question_by_id(self):
        print('Testing delete_question_by_id()')

        QuestionService.delete_question_by_id(questionId=1)
        answer = QuestionService.qet_all_questions_texts()

        self.assertEqual(len(answer), 1, 'rows count should be {0} actual {1}'.format(1, len(answer)))
        print('Successful\n')
    # =====================


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
