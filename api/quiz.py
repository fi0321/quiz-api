from persist import Persistance

class Quiz:
    """
        Use this class to create, read, update and delete quizzes.

        METHODS
        -------
            - createQuiz(): Create quiz using the Quiz Data Structure.
            - updateQuiz(): Update Quiz using the Quiz Data Structure
            - get_all_quiz(): Get all quiz as List
            - setStartDate(): Set the startTime Timestamp for a quiz
            - setEndDate(): Set the endTime Timestamp for a quiz.
            - setAuthors(): Set the User ID of those qho can modify thw quiz
            - removeAuthors(): Remove the User ID of one of the Authors who can 
                            modify the quiz.

        DATA STRUCTURES
        ---------------
           
        quizBank
        quizid:{
            QuizDataStructure
        },
        quizid:{
            QuizDataStructure
        },
        quizid:{
            QuizDataStructure
        }


        Quiz Data Structure = {
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


    """
    def __init__(self, testMode = False):
        self.persistApi = Persistance('quiz')
        self.persistApi.persist_quiz()
        if testMode:
            self.testMode = testMode
            self.persistApi = Persistance('quiz-test'+self.persistApi.generate_unique_id(10))

    def createQuiz(self,quizDs):
        """
        Create Quiz using the Quiz Data Structure

        PARAMETER
        ---------
            - Quiz Data Structure
        RETURNS
        -------
            - True: if succesful
        """
        return self.persistApi.create_quiz(quizDs)
        

    def updateQuiz(self,quizDs):
        """
        Update Quiz using the Quiz Data Structure.

        PARAMETER
        ---------
            - Quiz Data Structure
        RETURNS
        -------
            - True
            - False
        """
        return self.persistApi.modify_quiz(quizDs)

    def delete_quiz(self,id):
        """
        Delete the Quiz from Quiz List using the 
        Quiz Unique ID

        PARAMETER
        ---------
            - Quiz Unique ID: (Type: String)
        RETURNS
        -------
            - True: if Succesful
        """
        return self.persistApi.delete_quiz(id)

    def get_all_quiz(self):
        """
        Get the List of all quizzes.

        RETURNS
        -------
            - List of Quiz Data Structures
        """
        return self.persistApi.get_all_data_without_keys()

    def setStartDate(self,quizId,startDateTimestamp):
        """
        Modify the start date for a given Quiz

        PARAMETER
        ---------
            - Quiz Data Structure
            - startDateTimestamp: (Type: Integer)
                            new startTimestamp
        RETURNS
        -------
            - Quiz Data Structure
        """
        quiz = self.persistApi.retrieve_quiz(quizId)
        quiz['startTime'] = startDateTimestamp
        self.persistApi.modify_quiz(quiz)
        return quiz
    
    def setEndDate(self,quizId,endDateTimestamp):
        """
        Modify the end date for a given Quiz

        PARAMETER
        ---------
            - Quiz Data Structure
            - endDateTimestamp: (Type: Integer)
                            new endTimestamp
        RETURNS
        -------
            - Quiz Data Structure
        """
        quiz = self.persistApi.retrieve_quiz(quizId)
        quiz['endTime'] = endDateTimestamp
        self.persistApi.modify_quiz(quiz)
        return quiz

    def setAuthors(self,quizId,uid):
        """
        Set the Authors for a given quiz. An Author is a user 
        who can modify the quiz. By default all Insuctor are Authors.

        PARAMETER
        ---------
            - Quiz Unique ID:(Type: String)
                        Unique id of the quiz qhose access is to 
                        be modified.
            - User Unique ID: (Type: String)
                        Unique id of the user who is to be given the quiz access
        
        RETURNS
        -------
            - True: if Succesuful
            - False: if The Uid or QuizId is Invalid

        """
        quiz = self.persistApi.retrieve_quiz(quizId)
        if uid not in quiz['authors']:
            quiz['authors'].append(uid)
        else:
            return False
        self.persistApi.modify_quiz(quiz)
        return True

    def removeAuthors(self,quizId,uid):
        """
        Remove the Authors for a given quiz. An Author is a user 
        who can modify the quiz. By default all Insuctor are Authors.

        PARAMETER
        ---------
            - Quiz Unique ID:(Type: String)
                        Unique id of the quiz qhose access is to 
                        be modified.
            - User Unique ID: (Type: String)
                        Unique id of the user
        
        RETURNS
        -------
            - True: if Succesuful
            - False: if The Uid or QuizId is Invalid
        """
        quiz = self.persistApi.retrieve_quiz(quizId)
        if uid in quiz['authors']:
            quiz['authors'].remove(uid)
        else:
            return False
        self.persistApi.modify_quiz(quiz)
        return True

    def check_quiz_access(self,quizId,userId):
        """
        Check the access of the User for a given quiz. An Author is a user 
        who can modify the quiz. By default all Insuctor are Authors.

        PARAMETER
        ---------
            - Quiz Unique ID:(Type: String)
                        Unique id of the quiz qhose access is to 
                        be checked.
            - User Unique ID: (Type: String)
                        Unique id of the user who identified as Author
        
        RETURNS
        -------
            - True: if Succesuful
            - False: if The Uid or QuizId is Invalid
        """
        quiz = self.persistApi.retrieve_quiz(quizId)
        if userId in quiz['authors']:
            return True
        else:
            return False

    def destruct_testMode(self): 
        """
        Clean up after testing!
        """
        if self.testMode:
            self.persistApi.close()
            self.persistApi.remove_db()

    