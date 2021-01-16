import unittest
import sys
sys.path.append("./api")
from persist import Persistance


class TestPersistance(unittest.TestCase):

    def setUp(self):
        self.persistApiStudent = Persistance('student-test')
        self.persistApiInstructor = Persistance('instructor-test')
        self.persist_qbank = Persistance('question-bank-test'+(Persistance().generate_unique_id(12)))
        self.persist_quiz = Persistance('quiz-test'+str(Persistance().generate_unique_id(12)))
        # self.TestUser.setTestMode(1)
        for i in range(10):
            email = str(i)+"@"+str(i)+".com"
            password = "abc.xyz"+str(i)
            credentials = {
                "email": email,
                "password":password
            }
            self.persistApiStudent.add_new_data(credentials)
            self.persistApiInstructor.add_new_data(credentials)
        

    
    def test_get_all_keys(self):
        self.assertEqual(len(self.persistApiInstructor.get_all_keys()),len(self.persistApiStudent.get_all_keys()))
        self.assertNotEqual(self.persistApiInstructor.get_all_keys(),self.persistApiStudent.get_all_keys())


    def test_generate_unique_id(self):
        self.assertEqual(len(self.persistApiStudent.generate_unique_id()),len(self.persistApiInstructor.generate_unique_id()))
        self.assertNotEqual(self.persistApiStudent.generate_unique_id(),self.persistApiInstructor.generate_unique_id())

    def test_get_all_data(self):
        self.assertEqual(len(self.persistApiInstructor.get_all_data()),len(self.persistApiStudent.get_all_data()))
        self.assertNotEqual(self.persistApiInstructor.get_all_data(),self.persistApiStudent.get_all_data())

    def test_get_all_data_without_keys(self):
        self.assertEqual(len(self.persistApiInstructor.get_all_data_without_keys()),len(self.persistApiStudent.get_all_data_without_keys()))
        self.assertEqual(self.persistApiInstructor.get_all_data_without_keys(),self.persistApiStudent.get_all_data_without_keys())

    def test_check_login_credentials(self):
        cred = {
            "email":"2@2.com",
            "password":"abc.xyz2"
        }

        self.assertNotEqual(self.persistApiStudent.check_login_credentials(cred),0)
        self.assertNotEqual(self.persistApiInstructor.check_login_credentials(cred),0)

    def test_check_registration_credentails(self):
        cred = {
            "email":"somebody@somemail.com",
            "password":"somePassword123"
        }
        self.assertNotEqual(self.persistApiStudent.check_registration_credentials(cred),-1)
        self.assertNotEqual(self.persistApiInstructor.check_registration_credentials(cred),-1)
        self.assertNotEqual(self.persistApiStudent.check_login_credentials(cred),0)
        self.assertNotEqual(self.persistApiInstructor.check_login_credentials(cred),0)

    def test_remove_all_data(self):
        self.persistApiStudent.remove_all_data()
        self.persistApiInstructor.remove_all_data()

        self.assertEqual(len(self.persistApiStudent.get_all_data()),0)
        self.assertEqual(len(self.persistApiInstructor.get_all_data()),0)

    def test_persist_quiz(self):
        self.assertEqual(self.persistApiInstructor.persist_quiz(),1)

    def test_validate_question(self):
        question = "some question?"
        questionDs = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
        }
        self.assertEqual(self.persist_qbank.validate_question(questionDs),True)
        questionDs.pop('question')  #making data structure invalid
        self.assertEqual(self.persist_qbank.validate_question(questionDs),False)

    def test_validate_quiz(self):
        quizDataStructure = {
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
        self.assertEqual(self.persist_quiz.validate_quiz(quizDataStructure),True)
        quizDataStructure.pop('name')
        quizDataStructure.pop('questions')
        self.assertEqual(self.persist_quiz.validate_quiz(quizDataStructure),False)

    def test_create_quiz(self):
        quizDataStructure = {
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
        self.assertEqual(len(str(self.persist_quiz.create_quiz(quizDataStructure))),17)        
        newQuizDataStructure = {                # Testing an Invalid Data Structure   
            "QuizName":"some other question",   # wrong key
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
        self.assertEqual(self.persist_quiz.create_quiz(newQuizDataStructure),False)        
        
    def test_retrieve_quiz(self):
        self.assertEqual(self.persist_quiz.retrieve_quiz("123"),0)                  
        quizDataStructure = {
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
        qid = self.persist_quiz.create_quiz(quizDataStructure)
        self.assertEqual(self.persist_quiz.retrieve_quiz(qid),quizDataStructure)                       


    def test_modify_quiz(self):
        quizDataStructure = {
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
        qid = self.persist_quiz.create_quiz(quizDataStructure)
        quizData = self.persist_quiz.retrieve_quiz(qid)
        quizData['name'] = "new quiz!"
        self.assertEqual(self.persist_quiz.modify_quiz(quizData),True)

    def test_delete_quiz(self):
        quizDataStructure = {
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
        qid = self.persist_quiz.create_quiz(quizDataStructure)
        self.assertEqual(self.persist_quiz.delete_quiz(qid),True) 
        # can't delete the same object again       
        self.assertEqual(self.persist_quiz.delete_quiz(qid),False)        

        
    def test_create_question(self):
        question = "some question?"
        credentials = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
        }
        self.assertEqual(self.persist_qbank.create_question(credentials),True)
        invalidCredentials = {    #invalid data structure
            "SomeQuestion": question,
            "option":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
        }
        self.assertEqual(self.persist_qbank.create_question(invalidCredentials),False)
        
    def test_modify_question(self):
        question = "some question?"
        credentials = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
        }
        qid = self.persist_qbank.create_question(credentials)
        question = self.persist_qbank.get_all_data_without_keys()[0]
        question['question'] = "new question"
        self.assertEqual(self.persist_qbank.modify_question(question['id'],question),True)
        question.pop('question')  #making data structure invalid
        self.assertEqual(self.persist_qbank.modify_question(question['id'],question),False)

    def test_delete_question_from_questionbank(self):
        question = "some question?"
        credentials = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
        }
        self.persist_qbank.create_question(credentials)
        question = self.persist_qbank.get_all_data_without_keys()[0]
        
        self.assertEqual(self.persist_qbank.delete_question_from_questionbank(question['id']),True)
        self.assertEqual(self.persist_qbank.delete_question_from_questionbank('test-qid'),False)
    
#     def test_add_attemp_to_quiz(self):
#         self.assertEqual(self.persistApiInstructor.add_attemp_to_quiz(5),6)
    
#     def test_storing_responses_for_quiz(self):
#         self.assertEqual(self.persistApiInstructor.storing_responses_for_quiz([1,2,0]),True)
        
#     def test_create_qbank(self):
#        self.assertEqual(self.persistApiInstructor.create_qbank('some-qbank-name'),True)

#     def test_retrieve_qbank(self):
#         self.assertEqual(self.persistApiInstructor.retrieve_qbank('id'),True)

    def test_persist_qbank(self):
        self.assertEqual(self.persist_qbank.persist_qbank(),True)
        # self.persist_qbank.persist_qbank.close()
        # self.persist_qbank.persist_qbank.remove_db()

#     def test_get_quiz_attempts(self):
#         self.assertEqual(self.persistApiInstructor.get_quiz_attempts('sid','qid'),True)

    def tearDown(self):
        self.persistApiStudent.close()
        self.persistApiInstructor.close()
        self.persistApiStudent.remove_db()
        self.persistApiInstructor.remove_db()

        self.persist_qbank.close()
        self.persist_quiz.close()
        self.persist_qbank.remove_db()
        self.persist_quiz.remove_db()
    
if __name__ == "__main__":
    unittest.main()