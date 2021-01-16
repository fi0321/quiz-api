import unittest
import sys
sys.path.append("./api")
from quesbank import QuestionBank

class TestQuestionBank(unittest.TestCase):
    def setUp(self):
        self.persistApi = QuestionBank(1)
    #     self.persistApiInstructor = Persistance('instructor-test')

    #     # self.TestUser.setTestMode(1)
        for i in range(10):
            question = "some question"+str(i)+"?"
            credentials = {
                "question": question,
                "options":[{"opt":"op1","ans":False},
                           {"opt":"op2","ans":True},
                           {"opt":"op3","ans":False},
                           {"opt":"op4","ans":False}]
            }
            self.persistApi.add_question(credentials)
   
    def test_add_question(self):
        """
        Test for adding a question to question bank
        """
        self.assertEqual(len(self.persistApi.get_all_questions()),10)
        question = "some other question?"
        credentials = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                       {"opt":"op2","ans":True},
                       {"opt":"op3","ans":False},
                       {"opt":"op4","ans":False}]
        }
        self.persistApi.add_question(credentials)
        self.assertEqual(len(self.persistApi.get_all_questions()),11)

    def test_get_all_questions(self):
        """
        Test for getting all question from question bank
        """
        self.assertEqual(len(self.persistApi.get_all_questions()),10)

    def test_update_question_using_id(self):
        """
        Test for updating a question in question bank
        """
        data = self.persistApi.get_all_questions()
        id = data[0]['id']
        newQuestion = "modified question 1"
        data[0]['question'] = newQuestion
        self.persistApi.update_question_using_id(id,data)
        self.assertEqual(self.persistApi.get_all_questions()[0],data[0])

    def test_delete_data_using_id(self):
        """
        Test for deleting a question in question bank using Question 
        Unique Identifier
        """
        self.assertEqual(len(self.persistApi.get_all_questions()),10)
        self.persistApi.delete_data_using_id(self.persistApi.get_all_questions()[0]['id'])
        self.assertEqual(len(self.persistApi.get_all_questions()),9)

    def tearDown(self):
        self.persistApi.destruct_testMode()

if __name__ == "__main__":
    unittest.main()