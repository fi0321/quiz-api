from persist import Persistance
class QuestionBank:
    """
    Use this class to create, read, update and delete Questions
    from Question Bank

    METHODS
    -------
        - add_question(): Add Question to Question Bank using the
                        Question Data Structure.
        - get_all_questions(): Get the list of all questions stored
                        in the question bank.
        - update_question_using_id(): Update queston stored in the 
                        question bank using the Question Unique ID 
                        and Question Data Structure
        - delete_data_using_id(): Delete Question from the question
                        bank using the Question Unique ID.
        - destruct_testMode(): Made for testing purposes. Clean Up 
                        after testing.
    DATA STRUCTURE
    --------------
    questionbank
        qid
         -q1:id
         -q2:id
         -q3:id

        Question Data Structure = {
            "question": question,
            "options":[{"opt":"op1","ans":False},
                    {"opt":"op2","ans":True},
                    {"opt":"op3","ans":False},
                    {"opt":"op4","ans":False}]
            "id": Question Unique Id
        }
    """
    def __init__(self, testMode = False):
        self.persistApi = Persistance('question-bank')
        self.persistApi.persist_qbank()
        if testMode:
            self.testMode = testMode
            self.persistApi = Persistance('qb-test'+self.persistApi.generate_unique_id(10))

    def add_question(self,quesDs):
        """
        Add a new Question to question bank using Question Data 
        Structure.

        PARAMETER
        ---------
            - Question Data Structure
        RETURNS
        -------
            - Question Unique ID: (Type: String)
                            The Unique ID of the Question
        """
        # Question
        #     option []
        #     answer []

        qid = self.persistApi.create_question(quesDs)
        return qid

    def get_all_questions(self):
        """
        Get all the question from the Question bank
        as a List of Question Data Structures

        RETURNS
        -------
            - List of Question Data Structures
        """
        return self.persistApi.get_all_data_without_keys()

    def get_quetion_using_id(self,qid):
        print(qid)
        print(self.persistApi.get_data_using_key(qid))
        return self.persistApi.get_data_using_key(qid)

    def update_question_using_id(self,id,questionDs):
        """
        Update a Question in Question bank using the 
        Question Unique ID and Question Data Structure

        PARAMETER
        ---------
            - Question Unique ID: (Type: String)
            - Question Data Structure
        RETURNS
        -------
            - True: if succesful
        """
        self.persistApi.modify_question(id,questionDs)
        return True

    def delete_data_using_id(self,id):
        """
        Delete the question from Question bank using the 
        Question Unique ID

        PARAMETER
        ---------
            - Question Unique ID: (Type: String)
        RETURNS
        -------
            - True: if Succesful
        """
        return self.persistApi.delete_question_from_questionbank(id)

    def verifyQuestionAnswer(self,qid,answerList):
        
        optionsList = self.persistApi.get_data_using_key(qid).get('options');
        correct = True
        for i in optionsList:
            answer = optionsList[i].get('ans')
            
            if answer != answerList[i] and answerList[i] != 1:
                # check for questions with multiple correct answers
                # and the user has picked one right answer
                correct = False
                break
            # else

        return correct
        

    def destruct_testMode(self):
        """
        Clean up after testing!
        """ 
        if self.testMode:
            self.persistApi.close()
            self.persistApi.remove_db()
    