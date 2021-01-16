// alert("conected");


var optionsCount = 0;
var QuizLen = 0;
var QuesLen = [];
// var ans = [];
// function fetchQuestion() {

//     $.post("/get_question", function (quesListData) {
//         // alert(data);
//         var res = JSON.parse(quesListData);
//         res = JSON.parse(res.questionData);
//     })
// }

function setQuiz() {

    $.post("/get_quizzes", function (dt) {
        $.post("/get_question", function (quesListData) {
            // alert(data);
            var res = JSON.parse(quesListData);
            res = JSON.parse(res.questionData);
            console.log(res)
            if (quesListData == "error") {
                alert('Error!')
            } else {
                let data = JSON.parse(dt)
                // console.log(data)
                let quizDiv = document.getElementById('quiz-disp');
                let quizModalDiv = document.getElementById('quiz-list-quiz-modal');
                quizDiv.innerHTML = "";
                quizModalDiv.innerHTML = "";
                // questionsData = JSON.parse(questionsData.questionData)
                // console.log(data)
                // console.log(questionsData.length)
                let i = 0;
                QuizLen = data.quizData.length;
                for (i = 0; i < data.quizData.length; i++) {
                    let qdata = data.quizData[i];
                    let questionsHtml = "";
                    let q = 0;
                    QuesLen[i] = qdata.questions.length;
                    // console.log("qid", qdata.questions);
                    for (q = 0; q < qdata.questions.length; q++) {
                        var id = qdata.questions[q];
                        let p = 0;

                        for (p = 0; p < res.length; p++) {
                            if (id == res[p].id) {
                                // questionsHtml += res[i]
                                questionsHtml += `
                                    <p class="question-${i}-${q}">${res[p].question}</p>
                                    <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                    <div class="input-group-text">
                                    <input type="checkbox" class="opt-${i}-${q}">
                                    </div>
                                    </div>
                                    <p class="form-control option-p-${i}-${q}">${res[p].options[0].opt}</p>
                                    </div>

                                    <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                    <div class="input-group-text">
                                    <input type="checkbox" class="opt-${i}-${q}">
                                    </div>
                                    </div>
                                    <p class="form-control option-p-${i}-${q}">${res[p].options[1].opt}</p>
                                    </div>

                                    <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                    <div class="input-group-text">
                                    <input type="checkbox" class="opt-${i}-${q}">
                                    </div>
                                    </div>
                                    <p class="form-control option-p-${i}-${q}">${res[p].options[2].opt}</p>
                                    </div>

                                    <div class="input-group mb-3">
                                    <div class="input-group-prepend">
                                    <div class="input-group-text">
                                    <input type="checkbox" class="opt-${i}-${q}">
                                    </div>
                                    </div>
                                    <p class="form-control option-p-${i}-${q}">${res[p].options[3].opt}</p>
                                    </div>

                                    <hr>
                                `
                            }
                        }

                        // questionsHtml += qdata.questions[q] + " " + q + "<br>";
                    }
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
                        
                        <button id="quiz-take-btn-${i + 1}" type="button" class="btn btn-info" data-toggle="modal"
                        data-target="#q-attempt-modal-${i + 1}">check attempts</button>


                        <button id="quiz-take-btn-${i + 1}" type="button" class="btn btn-dark" data-toggle="modal"
                        data-target="#take-quiz-${i + 1}">Take Quiz</button>
                        
                    </div>
                    </div>
                </div>
        
            </div>
            `
                    quizModalDiv.innerHTML +=
                        `
                <div class="modal fade" id="take-quiz-${i + 1}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle">Take Quiz ${i + 1}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    ${questionsHtml}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-submit-result-quiz btn-primary">Submit</button>
                </div>
            </div>
        </div>
    </div>
            `

                }

                let j = 0;
                if (data.quizData.length == 0) {
                    quizDiv.innerHTML = "Quizzess will be displayed here!";
                }
            }

            //write functions here
            submitQuizAction();

        })
        // $(".questions").html(data);
    });


}

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

function submitQuizAction() {
    for (let w = 0; w < document.getElementsByClassName('btn-submit-result-quiz').length; w++) {
        console.log({ w })
        document.getElementsByClassName('btn-submit-result-quiz')[w].addEventListener('click', function () {
            alert('submitting quiz');
            let x = w;
            let qns = []

            // for (let x = 0; x < QuizLen; x++) {
            for (let y = 0; y < QuesLen[w]; y++) {

                let question = document.getElementsByClassName(`question-${x}-${y}`)[0].innerHTML;
                let optionsChk = document.getElementsByClassName(`opt-${x}-${y}`);
                let optionsPara = document.getElementsByClassName(`option-p-${x}-${y}`);

                let opt = [];

                for (let z = 0; z < optionsChk.length; z++) {
                    console.log(z)
                    if (optionsChk[z].checked) {
                        opt[z] = {
                            option: optionsPara[z].innerHTML,
                            answer: true
                        }
                    } else {
                        opt[z] = {
                            option: optionsPara[z].innerHTML,
                            answer: false
                        }
                    }
                }

                qns[y] = {
                    question,
                    options: opt
                }
            }
            // }
            ans = {
                questions: qns
            }
            let data = {
                id: document.getElementById(`quiz-id-${x + 1}`).innerHTML,
                attemptedOn: Date.now(),
                data: ans
            }
            // alert(JSON.stringify(ans))
            // console.log(ans)
            saveQuizAttempt(data)
            $(`#take-quiz-${w + 1}`).modal('hide');
        })
    }
}

function saveQuizAttempt(data) {

    $.ajax({
        type: "POST",
        url: "/save_quiz_attempt",
        data: JSON.stringify(data),
        success: function (a, b, c) {
            // alert('hey');
            // alert('data: ' + a, b, c);
            alert('succesfully submited quiz result')
            // getQuizAttempt()
            location.reload();
            // $(modal).modal('hide');
            // setQuiz()
        },
        error: function (data) { console.log("error!", data); },
        contentType: "application/json",
        dataType: 'json'
    });
}

function getQuizAttempt() {
    // alert('hey')
    $.post("/retrive_quiz_attempt", function (attemptData) {
        var res = JSON.parse(attemptData);
        // res = JSON.parse(res);
        // alert(attemptData);

        alert("Loading quiz and quiz attempt data complete!");
        console.log({ res })

        setQuizAttemptIntoUi(res.qattempt)
    })
}

function setQuizAttemptIntoUi(data, w = document.getElementsByClassName('btn-submit-result-quiz').length) {
    let qzModal = document.getElementById('attempt-modals');
    let quizId = [];
    qzModal.innerHTML = "";
    for (let ij = 0; ij < w; ij++) {
        console.log({ ij });
        let id = document.getElementById(`quiz-id-${ij + 1}`).innerHTML;
        quizId[ij] = id;
        // alert('hey w')
        qzModal.innerHTML += ` 
        <div class="modal fade bg-dark" id="q-attempt-modal-${ij + 1}" tabindex="-1" role="dialog" aria-labelledby="attempt-modal" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">View Quiz Attempt</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                    </div>
                    <p>Options <span class="user-selected">highlighted</span> are the inputs given by the user.
                    <div class="modal-body">
                        <div id="attempt-html-${ij + 1}"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
     `;


    }

    for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < w; j++) {
            // alert(quizId[j])
            if (data[i].id == quizId[j]) {
                console.log('matched')
                let attemptHtml = document.getElementById(`attempt-html-${j + 1}`);

                let questionHtml = "";

                for (let k = 0; k < data[i].data.questions.length; k++) {

                    let opt = "";

                    for (let l = 0; l < data[i].data.questions[k].options.length; l++) {

                        opt += `
                            <li><span class="${(data[i].data.questions[k].options[l].answer) ? "user-selected" : ""}">&nbsp;&nbsp;${data[i].data.questions[k].options[l].option}&nbsp;&nbsp;</span></li>
                        `
                    }

                    let optionsHtml = `
                        <ul>
                            ${opt}
                        </ul>
                    `;

                    questionHtml += `
                        <p>${k + 1}. ${data[i].data.questions[k].question}</p>
                        ${optionsHtml}
                    `
                }



                attemptHtml.innerHTML += `
                    <p><em>Attempt on ${convertDate(data[i].attemptedOn)}</p>
                    <hr>
                    ${questionHtml}

                `;
            }
        }
    }


}

window.onload = function () {
    setQuiz()
    // submitQuizAction();
    getQuizAttempt();
};

// getQuizAttempt()

