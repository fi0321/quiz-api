import unittest
import sys
sys.path.append("./api")
from user import User


class TestPersistance(unittest.TestCase):

    # def setUp(self):
    #     self.persistApiStudent = Persistance('student-test')
    #     self.persistApiInstructor = Persistance('instructor-test')

    #     # self.TestUser.setTestMode(1)
    #     for i in range(10):
    #         email = str(i)+"@"+str(i)+".com"
    #         password = "abc.xyz"+str(i)
    #         credentials = {
    #             "email": email,
    #             "password":password
    #         }
    #         self.persistApiStudent.add_new_data(credentials)
    #         self.persistApiInstructor.add_new_data(credentials)

    def test_registerUserUsingEmail(self):  
        """
        Test for Creating a new user
        """  
        TestUserReg = User(1) 
        credentials = {
            "email": "abc@xyz.com",
            "password": "abc.123"
        }
        authStudent = TestUserReg.registerUserUsingEmail(credentials.get('email'),credentials.get('password'))
        authUser = TestUserReg.registerUserUsingEmail(credentials.get('email'),"password")
        authAnotherUser = TestUserReg.registerUserUsingEmail(credentials.get('email'),'ab12')
        # print("register",authStudent)
        self.assertEqual(len(str(authStudent)),32)
        self.assertEqual(authUser,-1)
        self.assertEqual(authAnotherUser,0)
        TestUserReg.destruct_testMode()        

    def test_loginUserUsingEmail(self):
        """
        Test for logging in a user
        """
        TestUserLogin = User(1) 
        credentials = {
            "email": "abc@xyz.com",
            "password": "abc.123"
        }
        TestUserLogin.registerUserUsingEmail(credentials.get('email'),credentials.get('password'))

        authStudent = TestUserLogin.loginUserUsingEmail(credentials.get('email'),credentials.get('password'))
        authUser = TestUserLogin.loginUserUsingEmail('test@xyz.com','abc123')
        authAnotherUser = TestUserLogin.loginUserUsingEmail(credentials.get('email'),'abc123')
        # print("login",authStudent)
        self.assertEqual(len(str(authStudent)),32)
        self.assertEqual(authUser,-1)
        self.assertEqual(authAnotherUser,0)
        TestUserLogin.destruct_testMode()

    # def tearDown(self):
    #     self.persistApiStudent.close()
    #     self.persistApiInstructor.close()
    #     self.persistApiStudent.remove_db()
    #     self.persistApiInstructor.remove_db()
    
if __name__ == "__main__":
    unittest.main()