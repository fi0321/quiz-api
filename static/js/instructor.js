// alert("conected");


var optionsCount = 0;

function addOptionDiv() {
    optionsCount++;
    document.getElementById('options-div').innerHTML += `
                            <div class="input-group mb-3">
                                <input id="opt-${optionsCount}" type="text" class="form-control options-inputs" placeholder="Option ${optionsCount}"
                                    aria-label="Option" aria-describedby="basic-addon2">
                                <div class="input-group-append">
                                    <span class="input-group-text" id="basic-addon${optionsCount}">
                                        <input type="checkbox" class="chk-opt-ans"name="Answer" id="ans-${optionsCount}">
                                    </span>
                                </div>
                            </div>
    `
}


addOptionDiv();
addOptionDiv();
addOptionDiv();
addOptionDiv();

document.getElementById('new-opt').addEventListener('click', function () {
    addOptionDiv()
})

// click action while saving the question
document.getElementById('submit-question').addEventListener('click', function () {
    var question = document.getElementById('ques-text').value;
    var optionsInput = document.getElementsByClassName('options-inputs');
    var chkAns = document.getElementsByClassName('chk-opt-ans');
    var options = [];
    for (var i = 0; i < optionsInput.length; i++) {
        options[i] = {
            "opt": optionsInput[i].value,
            "ans": chkAns[i].checked
        }
    }

    // alert(JSON.stringify(question), options);
    // console.log(options)

    var data = {
        question,
        options: options
    }
    $.ajax({
        type: "POST",
        url: "/add_question",
        data: JSON.stringify(data),
        success: function (a, b, c) {
            // alert('hey');
            // alert('data: ' + a, b, c);
            // alert('added question')
            setQuestions()
            $('#add-ques').modal('hide');
        },
        error: function (data) { console.log("error!", data); },
        contentType: "application/json",
        dataType: 'json'
    });
})

function fetchQuestions() {
    $.post("/get_question", function (data) {
        var questionsData = JSON.parse(data);
        questionData = JSON.parse(data.questionData)
        return questionsData;
    })
}
// set the questions
function setQuestions() {
    $.post("/get_question", function (dt) {
        questionsData = JSON.parse(dt)
        console.log(questionsData)
        let questionsDiv = document.getElementById('ques-disp');
        let quizQuestionSelectDiv = document.getElementById('questions-list-quiz-modal');
        let editQuizQuestionDiv = document.getElementById('questions-list-quiz-edit');
        editQuizQuestionDiv.innerHTML = "";
        quizQuestionSelectDiv.innerHTML = "";
        questionsDiv.innerHTML = "";
        questionsData = JSON.parse(questionsData.questionData)
        // console.log(questionsData)
        // console.log(questionsData.length)
        let i = 0;
        for (i = 0; i < questionsData.length; i++) {
            let qdata = questionsData[i];
            let ans = []
            let optionsHtml = ""
            console.log(JSON.stringify(qdata));
            let j = 0;
            for (j = 0; j < qdata.options.length; j++) {
                optObj = qdata.options[j]
                if (optObj.ans) {
                    ans[j] = "ans-correct btn-success"
                } else {
                    ans[j] = "ans-wrong"
                }

                optionsHtml += `
                <li>
                    <span class="option ${ans[j]}">${optObj.opt}</span>
                </li>
                `
            }

            quizQuestionSelectDiv.innerHTML += `
            <div class="input-group mb-3">
                <span id="quiz-modal-question-id-${i + 1}" class="quiz-question-select-id-create hidden text-hidden">${qdata.id}</span>
                <div class="input-group-prepend">
                    <div class="input-group-text">
                        <input id="quiz-ques-sel-chkbox-${i + 1}" type="checkbox" class="quiz-question-select-chkbox">
                    </div>
                </div>
                <p class="form-control">${i + 1}. ${qdata.question}</p>
            </div>
            `
            editQuizQuestionDiv.innerHTML += `
            <div class="input-group mb-3">
                <span id="edit-quiz-modal-question-id-${i + 1}" class="edit-quiz-question-select-id hidden text-hidden">${qdata.id}</span>
                <div class="input-group-prepend">
                    <div class="input-group-text">
                        <input id="edit-quiz-ques-sel-chkbox-${i + 1}" type="checkbox" class="edit-quiz-question-select-chkbox">
                    </div>
                </div>
                <p class="form-control">${i + 1}. ${qdata.question}</p>
            </div>
            `

            questionsDiv.innerHTML +=
                `
                                        <div class="row">
                                            <div class="col-md-10">
                                                <p>
                                                    <span id="question-id-${i + 1}"class="hidden text-hidden">${qdata.id}</span>
                                                    ${i + 1}. ${qdata.question}
                                                </p>
                                            </div>
                                            <div class="col-md-2">

                                                <div class="btn-group" role="group" aria-label="Basic example">
                                                    <button type="button" class="btn btn-light" data-toggle="modal"
                                                        data-target="#ques-info-${i + 1}"><i class="fas fa-info"></i></button>
                                                    <!--<button type="button" class="btn btn-light" data-toggle="modal"
                                                        data-target="#ques-edit-${i + 1}"><i class="fas fa-pen"></i></button>-->
                                                    <button type="button" class="btn btn-danger" data-toggle="modal"
                                                        data-target="#ques-del-${i + 1}"><i class="fas fa-trash-alt"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>

                                        <div class="modal-disp">

                                            <div class="modal fade" id="ques-info-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h3 class="modal-title" id="exampleModalLabel">Question Info
                                                            </h3>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            <h5>${qdata.question}</h5>
                                                            <ul>
                                                                ${optionsHtml}
                                                            </ul>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="modal fade" id="ques-edit-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="exampleModalLabel">Edit this
                                                                question
                                                            </h5>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            ...
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            <button type="button" class="btn btn-primary">Save
                                                                changes</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="modal fade" id="ques-del-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="exampleModalLabel">Delete
                                                                Question
                                                            </h5>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Are you sure you want to delete this question?
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            <button id="delete-question-${i + 1}"type="button" class="btn btn-danger">Delete</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
            `

        }

        for (i = 0; i < questionsData.length; i++) {
            let j = i
            let id = `delete-question-${j + 1}`;
            let deleteQuestionButton = document.getElementById(id)
            deleteQuestionButton.addEventListener('click', function () {
                let id = document.getElementById(`question-id-${j + 1}`).innerText;
                // alert(j + 1,id)
                let data = {
                    id
                }
                $.ajax({
                    type: "POST",
                    url: "/delete_question",
                    data: JSON.stringify(data),
                    success: function (a, b, c) {
                        // alert('hey');
                        // alert('data: ' + a, b, c);
                        // alert('done')
                        $(`#ques-del-${j + 1}`).modal('hide');
                        setQuestions()
                    },
                    error: function (data) { console.log("error!", data); },
                    contentType: "application/json",
                    dataType: 'json'
                });
            })
        }
        if (questionsData.length == 0) {
            questionsDiv.innerHTML = "Questions will be displayed here!";
            quizQuestionSelectDiv.innerHTML = "Questions will be displayed here!";
        }
        // $(".questions").html(data);
    });
}

function setQuiz() {
    // $.post("/get_quizzes", function (dt) {
    //     var data = JSON.parse(dt)
    //     alert(data)
    //     console.log(data)
    //     // console.log(questionsData)
    //     let quizDiv = document.getElementById('quiz-disp');
    //     // let quizQuestionSelectDiv = document.getElementById('questions-list-quiz-modal');
    //     quizDiv.innerHTML = "";
    //     // questionsDiv.innerHTML = "";
    //     // data = JSON.parse(data.quizData)
    //     alert(JSON.stringify(data))

    // });

    $.post("/get_quizzes", function (dt) {
        data = JSON.parse(dt)
        console.log(data)
        let quizDiv = document.getElementById('quiz-disp');
        let quizModalDiv = document.getElementById('quiz-list-quiz-modal');
        quizDiv.innerHTML = "";
        quizModalDiv.innerHTML = "";
        // questionsData = JSON.parse(questionsData.questionData)
        // console.log(questionsData)
        // console.log(questionsData.length)
        let i = 0;
        for (i = 0; i < data.quizData.length; i++) {
            let qdata = data.quizData[i];
            // let ans = []
            // let optionsHtml = ""
            // console.log(JSON.stringify(qdata));
            // let j = 0;
            // for (j = 0; j < qdata.options.length; j++) {
            //     optObj = qdata.options[j]
            //     if (optObj.ans) {
            //         ans[j] = "ans-correct btn-success"
            //     } else {
            //         ans[j] = "ans-wrong"
            //     }

            //     optionsHtml += `
            //     <li>
            //         <span class="option ${ans[j]}">${optObj.opt}</span>
            //     </li>
            //     `
            // }

            quizDiv.innerHTML += `

            <div class="col-md-4 my-4">
                <div class="card h-100">
                    <span id="quiz-id-${i + 1}" class="quiz-question-select-id hidden text-hidden">${qdata.id}</span>
                    <div class="card-header">
                        ${i + 1}. ${qdata.name}
                    </div>
                    <div class="card-body">

                    <!-- <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Sapiente esse necessitatibus neque.</p> -->

                    Created on:&nbsp;&nbsp;&nbsp;&nbsp;${convertDate(qdata.createdOn)} <br>
                    Start date:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${convertDate(qdata.startTime)}<br>
                    End date:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${convertDate(qdata.endTime)}
                    <br><br>
                    No. of Questions: ${qdata.questions.length}

                    </div>
                    <div class="card-footer">
                        
                    <div class="btn-group float-right" role="group" aria-label="Basic example">
                        <!--<button type="button" class="btn btn-dark" data-toggle="modal"
                        data-target="#quiz-info-${i + 1}"><i class="fas fa-info"></i></button>-->
                        <button id="quiz-edit-btn-${i + 1}" type="button" class="btn btn-dark" data-toggle="modal"
                        data-target="#edit-quiz"><i class="fas fa-pen"></i></button>
                        <button type="button" class="btn btn-danger" data-toggle="modal"
                        data-target="#quiz-del-${i + 1}"><i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                    </div>
                </div>
        
            </div>
            `
            quizModalDiv.innerHTML +=
                `
                                        <div class="modal-disp">
                                            <div class="modal fade" id="quiz-info-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h3 class="modal-title" id="exampleModalLabel">Question Info
                                                            </h3>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            <h5>${qdata.name}</h5>
                                                            <ul>
                                                                ${i}
                                                            </ul>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="modal fade" id="quiz-edit-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="exampleModalLabel">Edit this
                                                                question
                                                            </h5>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            ...
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            <button type="button" class="btn btn-primary">Save
                                                                changes</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="modal fade" id="quiz-del-${i + 1}" tabindex="-1" role="dialog"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="exampleModalLabel">Delete
                                                                Quiz
                                                            </h5>
                                                            <button type="button" class="close" data-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Are you sure you want to delete this quiz?
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-dismiss="modal">Close</button>
                                                            <button id="delete-quiz-${i + 1}"type="button" class="btn btn-danger">Delete</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
            `

        }

        let j = 0;
        for (j = 0; j < data.quizData.length; j++) {
            // let i = j;
            let id = `delete-quiz-${j + 1}`;
            let qid = `quiz-edit-btn-${j + 1}`;
            // console.log("j", j)
            let qds = data.quizData[j];
            let quizid = qds.id;
            let name = qds.name;
            let createdOnTS = qds.createdOn;
            let createdOn = convertDate(qds.createdOn, 1)
            let startTime = convertDate(qds.startTime, 1)
            let endTime = convertDate(qds.endTime, 1)
            let authors = qds.authors;


            let editQuiz = document.getElementById(qid);
            let deleteQuizButton = document.getElementById(id)

            editQuiz.addEventListener('click', function () {
                // alert(JSON.stringify(data))
                // console.log("j", j)

                // console.log(data.quizData, qds)


                document.getElementById('edit-quiz-name').value = name;
                document.getElementById('edit-start-date').innerText = startTime;
                document.getElementById('edit-end-date').value = endTime;
                document.getElementById('quiz-edit-id').innerHTML = quizid;
                document.getElementById('quiz-edit-authors').innerHTML = authors;
                document.getElementById('quiz-edit-createdOn').innerText = parseInt(createdOnTS);
                // alert("details:  "+ quizid+ name+ startTime+ endTime)
                // console.log(quizid, name, startTime, endTime);

            })

            let idTemp = `quiz-id-${j + 1}`;
            let modal = `#quiz-del-${j + 1}`;
            deleteQuizButton.addEventListener('click', function () {
                
                console.log(idTemp)
                let id = document.getElementById(idTemp).innerText;
                
                let data = {
                    id
                }
                $.ajax({
                    type: "POST",
                    url: "/delete_quiz",
                    data: JSON.stringify(data),
                    success: function (a, b, c) {
                        // alert('hey');
                        // alert('data: ' + a, b, c);
                        // alert('done')
                        $(modal).modal('hide');
                        setQuiz()
                    },
                    error: function (data) { console.log("error!", data); },
                    contentType: "application/json",
                    dataType: 'json'
                });
            })
        }
        if (data.quizData.length == 0) {
            quizDiv.innerHTML = "Quizzess will be displayed here!";
        }
        // $(".questions").html(data);
    });


}
function saveQuiz(type) {
    document.getElementById('save-quiz-details').addEventListener('click', function () {
        var quizname = document.getElementById('quiz-name').value;
        var startDate = new Date(document.getElementById('start-date').value).getTime();
        var endDate = new Date(document.getElementById('end-date').value).getTime();
        var createdOn = Date.now()
        var questionsIds = []
        var ids = document.getElementsByClassName('quiz-question-select-id-create');
        var checkBoxes = document.getElementsByClassName('quiz-question-select-chkbox');
        var i = 0;
        for (i = 0; i < checkBoxes.length; i++) {
            var checkBox = checkBoxes[i];
            var qid = ids[i].innerText;
            if (checkBox.checked) {
                questionsIds.push(qid);
            }
        }
        if (quizname != null && quizname != "" && !isNaN(startDate) && !isNaN(endDate) && questionsIds.length > 0) {
            // console.log(quizname, startDate, endDate, createdOn, questionsIds)
            let data = {
                "name": quizname,
                "questions": questionsIds,
                "startTime": startDate,
                "endTime": endDate,
                "createdOn": createdOn,
                "authors": []
            }
            $.ajax({
                type: "POST",
                url: "/add_quiz",
                data: JSON.stringify(data),
                success: function (a, b, c) {
                    // alert('hey');
                    // alert('data: ' + a, b, c);
                    $('#create-quiz').modal('hide');

                    setQuiz()
                },
                error: function (data) { console.log("error!", data); },
                contentType: "application/json",
                dataType: 'json'
            });
        } else {
            alert('Invalid Input! Please enter correct data')
        }
    })
}


function deleteQuestion(id) {
    let data = {
        id
    }
    $.ajax({
        type: "POST",
        url: "/delete_question",
        data: JSON.stringify(data),
        success: function (a, b, c) {
            // alert('hey');
            // alert('data: ' + a, b, c);
            setQuestions()
        },
        error: function (data) { console.log("error!", data); },
        contentType: "application/json",
        dataType: 'json'
    });
}
setQuestions()
setQuiz()
saveQuiz(0)

document.getElementById('save-edited-quiz-details').addEventListener('click', function () {
    var id = document.getElementById('quiz-edit-id').innerHTML;
    var quizname = document.getElementById('edit-quiz-name').value;
    var startDate = new Date(document.getElementById('edit-start-date').value).getTime();
    var endDate = new Date(document.getElementById('edit-end-date').value).getTime();
    var authors = document.getElementById('quiz-edit-authors').innerHTML;
    var createdOn = document.getElementById('quiz-edit-createdOn').innerText;
    var questionsIds = []
    var ids = document.getElementsByClassName('edit-quiz-question-select-id');
    var checkBoxes = document.getElementsByClassName('edit-quiz-question-select-chkbox');
    var i = 0;
    for (i = 0; i < checkBoxes.length; i++) {
        var checkBox = checkBoxes[i];
        var qid = ids[i].innerText;
        if (checkBox.checked) {
            questionsIds.push(qid);
        }
    }
    if (quizname != null && quizname != "" && !isNaN(startDate) && !isNaN(endDate) && questionsIds.length > 0) {
        // console.log(quizname, startDate, endDate, createdOn, questionsIds)
        let data = {
            "id": id,
            "name": quizname,
            "questions": questionsIds,
            "startTime": startDate,
            "endTime": endDate,
            "createdOn": parseInt(createdOn),
            "editedOn": Date.now(),
            "authors": authors
        }
        $.ajax({
            type: "POST",
            url: "/edit_quiz",
            data: JSON.stringify(data),
            success: function (a, b, c) {
                // alert('hey');
                // alert('data: ' + a, b, c);
                $('#edit-quiz').modal('hide');

                setQuiz()
            },
            error: function (data) { console.log("error!", data); },
            contentType: "application/json",
            dataType: 'json'
        });
    } else {
        alert('Invalid Input! Please enter correct data')
    }
})
function convertDate(timestamp, type = 0) {
    var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    var todate = new Date(timestamp).getDate();
    var tomonth = month[new Date(timestamp).getMonth()];
    var toyear = new Date(timestamp).getFullYear() % 2000;
    var original_date = todate + " " + tomonth + " '" + toyear;
    if (type == 1) {
        var month = new Date(timestamp).getMonth() + 1;
        var year = new Date(timestamp).getFullYear();
        original_date = todate + "/" + month + "/" + year;
    }
    return original_date
}
// todo

// make set quiz
// and feed back modify and delete quiz



