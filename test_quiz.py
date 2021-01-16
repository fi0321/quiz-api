import unittest
import sys
sys.path.append("./api")
from quiz import Quiz

class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.quizApi = Quiz(1)
        quiz = {
            "name":"q1",
            "questions":[
                "qid1","qid2","qid3","qid4"
            ],
            "startTime":123456789,
            "endTime":999999999,
            "createdOn":100000000,
            "authors":[
                "uid1","uid2","uid3","uid4"
            ]
        }
        for i in range(10):
            self.quizApi.createQuiz(quiz)
    
    def test_create_quiz(self):
        """
        Test for creation of quiz
        """
        self.assertEqual(len(self.quizApi.get_all_quiz()),10)
        quiz = {
            "name":"q11",
            "questions":[
                "qid1","qid2","qid3","qid4"
            ],
            "startTime":123456789,
            "endTime":999999999,
            "createdOn":100000000,
            "authors":[
                "uid1","uid2","uid3","uid4"
            ]
        }
        self.quizApi.createQuiz(quiz)
        self.assertEqual(len(self.quizApi.get_all_quiz()),11)

    def test_update_quiz(self):
        """
        Test for updation of quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        quizData["name"] = "new quiz name"
        self.quizApi.updateQuiz(quizData)
        self.assertEqual(self.quizApi.get_all_quiz()[0],quizData)

    def test_get_all_quiz(self):
        """
        Test to get all quiz data as List
        """
        quizzes = self.quizApi.get_all_quiz()
        self.assertEqual(len(quizzes),10)
        quiz = {
            "name":"q11",
            "questions":[
                "qid1","qid2","qid3","qid4"
            ],
            "startTime":123456789,
            "endTime":999999999,
            "createdOn":100000000,
            "authors":[
                "uid1","uid2","uid3","uid4"
            ]
        }
        self.quizApi.createQuiz(quiz)
        self.assertEqual(len(quizzes),10)

    def test_setStartDate(self):
        """
        Test to set and modify the startDate Timestamp for a quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        self.assertEqual(quizData['startTime'],123456789)
        self.quizApi.setStartDate(quizData['id'],20000000)
        self.assertEqual(quizData['startTime'],20000000)

    def test_setEndDate(self):
        """
        Test to set and modify the endDate Timestamp for a quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        self.assertEqual(quizData['endTime'],999999999)
        self.quizApi.setEndDate(quizData['id'],20000000)
        self.assertEqual(quizData['endTime'],20000000)

    def test_setAuthors(self):
        """
        Test to set an author to a quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        self.assertEqual(self.quizApi.setAuthors(quizData['id'],"uid1"),0)
        self.assertEqual(self.quizApi.setAuthors(quizData['id'],"some-new-uid"),1)
        
    def test_removeAuthors(self):
        """
        Test to remove an author from a quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        self.assertEqual(self.quizApi.removeAuthors(quizData['id'],"uid1"),1)
        self.assertEqual(self.quizApi.removeAuthors(quizData['id'],"some-other-uid"),0)

    def test_check_quiz_access(self):
        """
        Test to check modify access for a quiz
        """
        quizData = self.quizApi.get_all_quiz()[0]
        self.assertEqual(self.quizApi.check_quiz_access(quizData['id'],"uid1"),1)
        self.assertEqual(self.quizApi.check_quiz_access(quizData['id'],"some-other-uid"),0)

    def tearDown(self):
        self.quizApi.destruct_testMode()

if __name__ == "__main__":
    unittest.main()