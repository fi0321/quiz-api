"""
Defines the persistance of data that will be used from shelve
"""
import shelve
import string
import random
import sys
import os


class Persistance:
    """
    This class defines and maintains the persistance of data.

    METHODS
    -------
        - get_all_keys(): Get all unique dict keys in the shelve file

        - generate_unique_id(self, size, chars): Generate a unique key
                with a given key size.

        - add_new_data(data): Add new data as a unique entry to shelve
                file.

        - get_all_data(): Get the data snapshot from shelve file

        -  get_all_data_without_keys(): Get the dict data snapshot from
                shelve file.
        - remove_data_using_key(): Delete a data entry using a unique
                identifier.
        - remove_all_data(): Remove all data entries form a shelve file.

        - update_data_using_key(): Update a single data entry using a
                unique identifier.

        - remove_db(): Delete all shelve files.

        - close(): Close all shelve file cursors.

        - check_login_credentials(): check the credentials for logging in.

        - check_registration_credentials(): check the credentials for creating
                a new account.

        - validate_question(): Validate the Question Data Structure.
        
        - validate_quiz(): Validate the quiz data structure.

        - persist_quiz(): Creates or opens the quiz shelve file using internal shelve persist API

        - create_quiz(): Creates a quiz using the Quiz Data Structure

        - retrieve_quiz(): Retrieves quiz with Quiz Unique Identifier

        - modify_quiz(): Modify the quiz using Quiz Data Structure

        - delete_quiz(): Deletes quiz using Quiz Unique Identifier

        - create_question(): Create a question and store it in question bank using Question Data Structure

        - modify_question(): Modify the Question using Question Unique Identifier and Question Data Structure

        - delete_question_from_questionbank(): Delete Question from question bank using Question Unique Identifier

        - persist_qbank(): Creates the persist shelve file for Question Bank

    """

    def __init__(self, filename = "persist-check"):
        """Initialise the persistance class with @arg:filename"""
        self.blobfile = shelve.open(filename, writeback=True)
        self.filename = filename

    def get_all_keys(self):
        '''
        Get all key entries from the shelve file

        RETURNS
        -------
            - @dict:data:@element:Key::(Type: String)
                Dictionary of all the keys inside the shelve file.
        '''
        db = self.blobfile
        data = []
        for k in db:
            data.append(k)

        # return db.keys()
        return data

    def generate_unique_id(self, size=32, chars=string.ascii_uppercase + string.digits):
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
        # only to be use internally with shelve persist
        return ''.join(random.choice(chars) for _ in range(size))

    def add_new_data(self, data,DataId = "000000"):
        """
        Add new data as a unique entry to shelve file.

        PARAMETERS
        ----------
            - data: (Type: User_defined)
                Contains the data that is to be added to the file.

        RETURN
        ------
            - UNIQUEID: (TYPE: String),
                    Unique ID/key where data was added in the shelve
                    file.
        """
        
        if DataId == "000000":
            DataId = self.generate_unique_id()

        data["id"] = DataId
        self.blobfile[DataId] = data
        return DataId

    def get_all_data(self):
        """
        Get complete data as a shelve data snapshot.

        RETURN
        ------
            - DataSnapshot: (Type: Shelve Object)
                contains all the data in the shelve file.
        """
        data = self.blobfile
        return data

    def get_all_data_without_keys(self):
        """
        Get complete data from shelve file as a dict data snapshot
        without keys.

        RETURN
        ------
            - DataSnapshot: (Type: List Object)
                contains all the data of the shelve file as a List.
        """
        data = []
        for k in self.get_all_keys():
            data.append(self.blobfile[k])

        return data

    def remove_data_using_key(self, key):
        """
        Remove certain entry in the shelve file using the Unique Identifier

        PARAMETERS
        ----------
            - key: (Type: String)
                Contains the key value of the dictionary where the data is
                to be deleted.
        """
        self.blobfile.pop(key)

    def remove_all_data(self):
        """
        Completely remove all data from the shelve file.

        RETURNS
        -------
            - Status: (Type: Bool)
                returns True if Successful.
        """
        self.blobfile.clear()
        return True

    def update_data_using_key(self, key, data):
        """
        Update a data entry in the shelve file

        PARAMETERS
        ----------
            - key: (Type: String)
                Contains the key value of the dictionary where the data is
                to be updated.
        """
        db = self.get_all_data()
        if key in db:
        # self.blobfile[key] = data
            db[key] = data
            return True
        return False

    def get_data_using_key(self,key):
        db = self.get_all_data()

        if key in db:
            print("TRUE ============== get data")
            return db[key]
        print("FALSE ============== no data")
        return False

    def remove_db(self):
        """
        Delete all shelve related file
        """
        os.remove(self.filename+'.dat')
        os.remove(self.filename+'.bak')
        os.remove(self.filename+'.dir')

    def close(self):
        """
        Close the connnection from the shelve file.
        """
        self.blobfile.sync()
        self.blobfile.close()

    def check_login_credentials(self, credentials):
        """
        Check whether the provided credentials can be used to authenticate,
        If they are valid then return a valid Unique ID.

        PARAMETER
        ---------
            - credentials: (Type: Dictionary)
                - Structure:
                    {
                        "email":"abc@xyz.com",
                        "password":"abc123"
                    }
                Contains the email and password that needs to be validated
                for auth.

        RETURNS
        -------
            - @val(Int):0: Params provided are invalid

            - @val(String):UNIQUE_ID: Account was found with given credentials,
                    Login successful.

            -<id>: {
                id:<id>,
                qno:12
                question:"ques"
                op:[]
                ans:2
                
            }
        """
        db = self.get_all_data()

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

    def check_registration_credentials(self, credentials):
        """
        Check whether the provided credentials can be used to create a
        new account, if they are valid then create a new account and
        return the account's valid Unique ID.

        PARAMETER
        ---------
            - credentials: (Type: Dictionary)
                - Structure:
                    {
                        "email":"abc@xyz.com",
                        "password":"abc123"
                    }
                Contains the email and password that needs to be used for
                creating a new account.
        
        RETURNS
        -------
            - @val(Int):-1: Account already exists with the given credentials,
                    so a new account can't be created.

            - @val(String):UNIQUE_ID: Account was created Successfully, returns
                    a unique identifier
        """
        db = self.get_all_data()
        for k in db:
                # @variable:k is key
                # check if the email already exists
                if(db[k].get("email") == credentials["email"]):
                    # account with credentials already exists
                    return -1

        uid = self.add_new_data(credentials)
        return uid

    def validate_question(self,questionDataStruct):
        """
        Validate the Question Data Structure.

        PARAMETER
        ---------
            - Quiz Data Structure
        
        RETURNS
        -------
            - True: if the data structure provided is valid
            - False: if the data structure provided is invalid
        """
        if 'question' in questionDataStruct and 'options' in questionDataStruct:
            for i in range(len(questionDataStruct['options'])):
                option = questionDataStruct['options']
                if 'opt' in option[i] and 'ans' in option[i]:
                    return True
                else:
                    return False
        else:
            return False

    def validate_quiz(self,quizDataStructure):
        """
        Validate the quiz data structure.

        PARAMETER
        ---------
            - Quiz Data Structure
            
        RETURNS
        -------
            - True: if the data structure provided is valid
            - False: if the data structure provided is invalid
        """
        quizDs = quizDataStructure
        if 'name' in quizDs and 'questions' in quizDs and 'authors' in quizDs:
            return True
        else:
            return False

    # QUIZ
    def persist_quiz(self):
        """
        Creates or opens the quiz shelve file using internal shelve persist API
        
        
        RETURNS
        -------
            - True: if it is a success
        """
        filename = 'quiz'
        self.blobfile = shelve.open(filename, writeback=True)
        self.filename = filename
        return True

    def create_quiz(self,quizDs):
        """
        Creates a quiz using the Quiz Data Structure
        
        PARAMETER
        ---------
            - Quiz Data Structure: (Type: QuizDataStruc)

        RETURNS
        -------
            - Quiz Unique Id: (Type: String)
        """
        if self.validate_quiz(quizDs):
            return self.add_new_data(quizDs,"quiz-"+str(self.generate_unique_id(12)))
        else:
            return False
    
    def retrieve_quiz(self,quizid):
        """
        Retrieves quiz with Quiz Unique Identifier

        PARAMETER
        ---------
            - Quiz Unique Id:(Type: string)
        RETURNS
        -------
            - QuizData
            - False: if provided Quiz Unique Id is invalid
        """
        db = self.get_all_data()
        if quizid in db:
            return db[quizid]

        return False
        

    def modify_quiz(self, quizDs):
        """
        Modify quiz, retrieves the quiz from the storage, adds or removes details and stores it back again.
        
        PARAMETER
        ---------
            - Quiz Data Structure: (Type: QuizDataStruct)       
            
        RETURNS
        -------
            - True: if Successful
            - False: if provided Quiz Data Strucis invalid

        """
        if self.validate_quiz(quizDs):
            db = self.get_all_data()
            if quizDs['id'] in db:
                db[quizDs['id']]=quizDs
                return True
        return False

    def delete_quiz(self, quizid):
        """
        Deletes quiz using Quiz Unique Identifier

        PARAMETER
        ---------
            - Quiz Unique Id: Unique identifier for a quiz

        RETURNS
        -------
            - True: if Successful
            - False: if Qid is Invalid
        """
        db = self.get_all_data()
        if quizid in db:
            db.pop(quizid)
            return True

        return False

    # QUESTIONBANK
    def create_question(self, quesDs):

        """
        Create a question and store it in question bank using Question Data Structure

        PARAMETER
        ---------
            - Question Data Structure
        RETURNS
        -------
            - True
        """
        if self.validate_question(quesDs):
            self.add_new_data(quesDs,"question-"+str(self.generate_unique_id(12)))
            return True
        else: 
            return False
        
    def modify_question(self, qid, qDs):
        """
        Modify the Question using Question Unique Identifier and Question Data Structure

        PARAMETER
        ---------
            - Question Unique Id: (Type: String)
            - Question Data Structure

            
        RETURNS
        -------
            - True: if succesful
            - False: if failed
        """
        if self.validate_question(qDs):
            self.update_data_using_key(qid,qDs)
            return True
        else:
            return False
        
    

    def delete_question_from_questionbank(self,qid):
        """
        Delete Question from question bank using Question Unique Identifier

        PARAMETER
        ---------
            - Unique Question Identifier: (Type:String)
        RETURNS
        -------
            - True
            - False
        """
        db = self.get_all_data()
        if qid in db:
            self.remove_data_using_key(qid)
            return True
        return False

    # def add_attemp_to_quiz(self,attempt_count):

        
    #     pass
    
    # def storing_responses_for_quiz(self,responses):
    #     # True
    #     pass

    # def create_qbank(self, question_bank_name):
    #     """
    #     Params: question(a dictionary) 
    #     adds questions to a question bank which is a list or dictionary and generates a unique id for the qbank
        
    #     QbankData
    #     """
    #     pass

    # def retrieve_qbank(self,qbankid):
    #     """
    #     Params:qbankid
    #     retrieves qbank with uid
    
    #     List of QuestionData in Qbank
    #     """
    #     pass


    def persist_qbank(self):
        """
        Creates the persist shelve file for Question Bank

        RETURNS
        -------
            - True: if Successful
        """
        filename = 'question-bank'
        self.blobfile = shelve.open(filename, writeback=True)
        self.filename = filename
        return True

    def get_user_data(self,uid):
        """
        Get the user data using User Unique Identifier

        PARAMETER
        ---------
            - User Unique Identifier: (Type: String)

        RETURNS
        -------
            - User Data Structure
        """
        return self.get_data_using_key(uid)

    def set_user_data(self,uid,user):
        """
        Set the user data using User Data Structure

        PARAMETER
        ---------
            - User Data Structure

        RETURNS
        -------
            - True
            - False
        """
        return self.update_data_using_key(uid,user)

    # def get_quiz_attempts(self,studentId,quizId):
        
    #     """
        
    #     """
    #     pass
