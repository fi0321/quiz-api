import string
import random
from persist import Persistance
import hashlib
from quiz import Quiz
from quesbank import QuestionBank
# account type @params:accType
STUDENT = 1
INSTRUCTOR = 0
# actions @params:action
LOGIN = 1
REGISTER = 0

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    '''
    Generate a unique ID based on @param: size

    PARAMETERS
    ----------
        - SIZE: (TYPE: Int), Default Value = 12
                Describe the size of the generated ID
        - CHARS: (TYPE: String), Default Value = [0-9]&[A-Z]
                Define the characters that will be used to generate the unique ID
    
    RETURN
    ------
        - UNIQUEID: (TYPE: String), 
                Unique ID of string of size @param: size
    '''
    return ''.join(random.choice(chars) for _ in range(size))

def hashpw(pw):
    """
    Hash @param:pw and return hashed password
    
    PARAMETERS
    ----------
        - PW: (TYPE: String)
              Password that is to be hashed

    RETURN
    ------
        - hashed Password: (Type: String)
              Value of the hash of password with salt
    """
    # use a secret salt
    salt = "someSalt"
    # Hash the password
    passwd = pw+salt
    hasedPw = hashlib.sha512(passwd.encode()).hexdigest()
    # hasedPw = pw
    return hasedPw

class User:
    """
    Use this class to create both Student's account as well as 
    Instructor's account!
    
    METHODS
    -------
        - setTestMode(): Use this method for testing

        - registerUserUsingEmail(email,password,isInstructor):
                Register a new account using email, password and account
                type (Student/Instructor).

        - loginUserUsingEmail(email, password, isInstructor): 
                Login using email, password and account type (Student/Password).
    
    """
    def __init__(self,testMode = False):
        """
        Initialise the users class by creating an instance
        @var:debug and @var:testMode are defined for testing purposes
        and will be used while testing!
        """
        self.accType = STUDENT
        self.debug = False
        self.testMode = False
        if testMode:
            self.testMode = True
            self.debug = True
            self.persistApi = Persistance(id_generator(12)+'-test')

    # def setTestMode(self,testMode):
    #     """Created for testing purposes."""
    #     if testMode:
    #         self.testMode = True
    #         self.debug = True
    #     else:
    #         self.testMode = False
    #         self.debug = False


    def registerUserUsingEmail(self, email, password, isInstructor=False):
        """
        Create a new user using email, password and the account type. 
        If the account that is being created is an Instructor account 
        then pass @arg:isInstructor as True.
        
        PARAMETERS
        ----------
            - email: (Type:String)
                    It contains the String email
            
            - password: (Type: String)
                    It contains the plain text password

            - isInstructor: (Type: Bool), Default = False
                    It defines the type of account that is going to 
                    be created.
                    True => Instructor account
                    False => Student account

        RETURN
        ------
            - @val(Int):0: Params provided are invalid

            - @val(Int):-1: Account already exists with the given credentials,
                            so a new account can't be created.
            
            - @val(String):UNIQUE_ID: Account was created Successfully, returns 
                            a unique identifier

                        
        """
        if not isInstructor:
            self.accType = STUDENT
            if not self.testMode:
                self.persistApi = Persistance('student')
            # else:
            #     self.persistApi = Persistance('student-test')
        else:
            self.accType = INSTRUCTOR
            if not self.testMode:
                self.persistApi = Persistance('instructor')
            # else:
            #     self.persistApi = Persistance('instructor-test')
                
        if not (email != None and password != None and len(email)>6 and len(password) >=6):
            return 0

        credentials = {
            "email": email,
            "password": hashpw(password),
            "accType": self.accType,
            "quiz_attempts":[]
        }

        db = self.persistApi.get_all_data()
        for k in db:
                # @variable:k is key
                # check if the email already exists
                if(db[k].get("email") == credentials["email"]):
                    # account with credentials already exists
                    return -1

        uid = self.persistApi.add_new_data(credentials)
        return uid


        # authResult = self.persistApi.check_registration_credentials(credentials)

        # return authResult

    def loginUserUsingEmail(self, email, password, isInstructor=False):
        """
        Log in user using email, password and accountType.
        If the account that is being logged in is an Instructor account 
        then pass @arg:isInstructor as True.
        
        PARAMETERS
        ----------
            - email: (Type:String)
                    It contains the String email
            
            - password: (Type: String)
                    It contains the plain text password

            - isInstructor: (Type: Bool), Default = False
                    It defines the type of account that is going to 
                    be created.
                    True => Instructor account
                    False => Student account

        RETURN
        ------
            - @val(Int):0: Params provided are invalid

            - @val(Int):-1: No account found with the given credentials
            
            - @val(String):UNIQUE_ID: Account was found with given credentials,
                            Login successful.
            
        """
        if not isInstructor:
            self.accType = STUDENT
            if not self.testMode:
                self.persistApi = Persistance('student')
            # else:
            #     self.persistApi = Persistance('student-test')
        else:
            self.accType = INSTRUCTOR
            if not self.testMode:
                self.persistApi = Persistance('instructor')
            # else:
            #     self.persistApi = Persistance('instructor-test')

        credentials = {
            "email": email,
            "password": hashpw(password),
            "accType": self.accType
        }

        db = self.persistApi.get_all_data()

        for k in db:
            # id = k
            if(db[k].get("email") == credentials["email"]):
                db[k].get('id')
                if(db[k].get("password") == credentials["password"]):
                    # Successful login
                    return db[k].get('id')
                else:
                    # Invalid Credentials
                    return 0
        return -1


        # acc = False
        # authResult = self.persistApi.check_login_credentials(credentials)

        # if authResult != 0:
        #     acc = True
        #     return authResult
        # elif authResult == 0:
        #     return 0
        # if not acc and authResult == -1:
        #     "No acc found"
        #     return -1

    def storeQuizForUser(self,uid,QuizDs):
        """
        Store the quiz attempt made by the user

        PARAMETER
        ---------
            - Quiz Unique Identifier: (Type: key)

        RESULT
        ------
            - Quiz Data Structure
        """


        user = Persistance('student').get_user_data(uid)
        # store quiz attempts as list
        user['quiz_attempts'].append(QuizDs)
        return Persistance('student').update_data_using_key(uid,user)
        # for (ans,qid) in zip(QuizDs['ans'], QuizDs['questions']):
        #     qb = QuestionBank()
            # qb.verifyQuestionAnswer(qid,ans)

        # pass

    def retrive_quiz_for_user(self,uid):
        """
        Retrive the quiz data using Quiz Unique Identifier

        PARAMETER
        ---------
            - Quiz Unique Identifier: (Type: String)

        RETURNS
        -------
            - Quiz Attempts Data Structure
        """
        user = Persistance('student').get_user_data(uid)
        print(user['quiz_attempts'])
        return user.get('quiz_attempts')

    def destruct_testMode(self): 
        if self.testMode:
            self.persistApi.close()
            self.persistApi.remove_db()

