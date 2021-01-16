from functools import wraps
import sys
sys.path.append("./api")
from quiz import Quiz
from quesbank import QuestionBank
from user import User
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
import json


app = Flask(__name__, static_url_path='/static')
app.debug = True
@app.route('/')
def index():
    """
    Index Route: 
    Route: "/"

    Methods: GET

    Send the login page. 
    """
    return render_template('login.html')


@app.route('/session')
def sess():
    """
    Session Route:
    Route: "/session"

    Methods: GET

    Meant as a Debug route.
    Send all the session variables in @flask:session
    """
    return str(session.items())


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login Route:
    Route: "/login"

    Methods: GET, POST

    GET:
        -send the login template

    POST: 
        -read and validate the responses from the client
        -call for authhandlers => Login user
        Responses:
            -email: (Type:JSON)
                Contains the email of client
            -password: (Type:JSON)
                Contains the plain text password String
            -accType: (Type:JSON): Flag Variable
                Contains the account type

    """
    if request.method == 'POST':
        """ request api for login verification"""
        # get all the credentials from json body of request or from form
        # Note: use ajax or xhr to POST data to this route
        content = request.form  # Sample data content
        # get username or email, password and account Type
        # usr = content.username
        email = request.form.get('email')
        password = request.form.get('password')
        accType = request.form.get('accType')

        isInstructor = False
        if accType == "on":
            isInstructor = True
        else:
            isInstructor = False

        user = User()
        auth = user.loginUserUsingEmail(email, password, isInstructor)
        if auth != 0 and auth != -1 and auth:
            session['email'] = email
            session['accType'] = isInstructor
            session['logged_in'] = True
            session['uid'] = auth

            return redirect(url_for('dashboard'))
        else:
            session['logged_in'] = False
            session['uid'] = -2
            if auth == -1:
                message = "Account not found!"
                print(message)
                return render_template('login.html', error=message)

            elif auth == 0:
                message = "Invalid Email or Password"
                print(message)
                return render_template('login.html', error=message)

            else:
                return auth

    """send the login page"""
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register Route:
    Route: "/register"

    Methods: GET, POST

    GET:
        -send the register template

    POST: 
        -read and validate the responses from the client
        -call for authhandlers => Register new user
        Responses:
            -email: (Type:JSON)
                Contains the email of client
            -password: (Type:JSON)
                Contains the plain text password String
            -accType: (Type:JSON): Flag Variable
                Contains the account type

    """
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConf = request.form.get('passconf')
        accType = request.form.get('accType')

        isInstructor = False
        if accType == "on":
            isInstructor = True
        else:
            isInstructor = False
        if password == passwordConf:
            user = User()

            auth = user.registerUserUsingEmail(email, password, isInstructor)
            if auth != 0 and auth != -1 and auth:
                session['accType'] = isInstructor
                session['email'] = email
                session['logged_in'] = True
                session['uid'] = auth
                return redirect(url_for('dashboard'))
            else:
                session['logged_in'] = False
                session['uid'] = -2
                if auth == -1:
                    message = "Account already exists with the given credentials!"
                    print(message)
                    return render_template('register.html', error=message)
                elif auth == 0:
                    message = "Invalid Email or Password"
                    print(message)
                    return render_template('register.html', error=message)
                else:
                    return auth
        else:
            return render_template('register.html', error="Passwords do not match")

    return render_template('register.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        """
        Type: METHOD

        Check whether a user is already logged in.

        """
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/dashboard')
@is_logged_in
def testdashboard():
    message = request.args.get("message")
    return render_template('dashboard.html', message=message)


@app.route('/me')
@is_logged_in
def dashboard():
    """
    Dashboard Route:
    Type: Route

    Render the dashboard template depending on the account that is signed in
    """
    if session['accType']:
        return render_template('instructorDash.html', email=session['email'])
    else:
        return render_template('studentDash.html', email=session['email'])


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    """
    Logout Route: 
    Route: "/logout" 

    Methods: GET

    Logout the currently logged User.
    """
    session.clear()
    return redirect(url_for('login'))

# ==============API==============
@app.route('/add_question', methods=['POST'])
@is_logged_in
def addQues():
    """
    Add Question API ROUTE
    Methods = POST

    Add the question to question bank.
    """
    data = request.json
    # data2 = request.get_json()
    # print("=======")
    print(data)
    # print(data2)
    # print("===========");
    qb = QuestionBank()
    qid = qb.add_question(data)
    # print("id:",qid)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/get_question', methods=['POST'])
# @is_logged_in
def getQues():
    """
    Get all Question API ROUTE
    Methods = POST

    Get all the questions with their options stores in the question bank.
    """
    # qb = QuestionBank()
    questions = QuestionBank().get_all_questions()
    # print(questions)
    return json.dumps({'success': True, 'questionData': json.dumps(questions)}), 200, {'ContentType': 'application/json'}


@app.route('/get_questions_using_id', methods=['POST'])
@is_logged_in
def getQuesWithoutAnswers():
    """
    Get Question data API ROUTE
    Methods = "POST"

    Get Question Information using Question Unique Identifier
    """
    data = request.json
    # qb =
    qid = data["id"]
    ques = QuestionBank().get_quetion_using_id(qid)
    # return ques
    if ques:
        return json.dumps({'success': True, 'qdata': ques}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/delete_question', methods=['POST'])
@is_logged_in
def delete_question():
    """
    Delete question API ROUTE
    Methods = "POST"

    Delete Question Information using Question Unique Identifier
    """
    qb = QuestionBank()
    data = request.json
    print(data)
    qid = data['id']
    print(qid)
    delQues = qb.delete_data_using_id(qid)
    if delQues:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/add_quiz', methods=['POST'])
@is_logged_in
def addQuiz():
    """
    Add Quiz data API ROUTE
    Methods = "POST"

    Add Quiz Information using Quiz Data Structure
    """
    quiz = Quiz()
    data = request.json
    data['authors'].append(session['uid'])
    status = quiz.createQuiz(data)
    if status != False:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/get_quizzes', methods=['GET', 'POST'])
def getQuiz():
    """
    Get Quiz data API ROUTE
    Methods = "POST"

    Get all Quiz Information from Quiz().get_all_quiz() method.
    """
    quiz = Quiz()
    quizData = quiz.get_all_quiz()
    print(quizData)
    return json.dumps({'success': True, 'quizData': quizData}), 200, {'ContentType': 'application/json'}


@app.route('/delete_quiz', methods=['POST'])
@is_logged_in
def delQuiz():
    """
    Delete Quiz data API ROUTE
    Methods = "POST"

    Delete a Quiz Information using Quiz Unique Identifier.
    """
    quiz = Quiz()
    data = request.json
    # print(data)
    qid = data['id']
    # print(qid)
    delQuiz = quiz.delete_quiz(qid)
    if delQuiz:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/edit_quiz', methods=['POST'])
@is_logged_in
def editQuiz():
    """
    Edit Quiz data API ROUTE
    Methods = "POST"

    Edit Quiz Information using Quiz Data Structure
    """
    quiz = Quiz()
    data = request.json
    # print(data)
    qid = data['id']
    # print(qid)
    editQuiz = quiz.updateQuiz(data)
    if editQuiz:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/save_quiz_attempt', methods=['POST'])
@is_logged_in
def saveQuizAttempt():
    """
    Save Quiz attempts API ROUTE
    Methods = "POST"

    Save Quiz attempt Information in a branch in user data structure
    """
    quiz = User()
    data = request.json
    storeQuiz = quiz.storeQuizForUser(session['uid'], data)
    if storeQuiz:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/retrive_quiz_attempt', methods=['POST'])
@is_logged_in
def retriveQuizAttempt():
    """
    Get Quiz attempts data API ROUTE
    Methods = "POST"

    Get Quiz attempt Information from the users Data structure
    """
    quiz = User()
    storeQuiz = quiz.retrive_quiz_for_user(session['uid'])
    if storeQuiz:
        return json.dumps({'success': True, 'qattempt': storeQuiz}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/test', methods=['GET', 'POST'])
def testRoute():
    """
    Test Route:
    Route: "/test"

    Methods: GET, POST

    A test route meant to test the functionality of flask
    """
    if request.method == 'GET':
        # return 'GET'

        # url query
        query = request.args.get('q')

        if query:
            return query

        # just a test route
        # sampleroute: /text?q=<your-data>

    if request.method == 'POST':
        return "post"
    return "hey"


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
