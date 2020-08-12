for (let index = 0; index < quiz_questions.length; index++) {
    let answer = quiz_questions[index]['answers'].indexOf(quiz_questions[index]['answers'].filter(a => a['value'] == 1)[0])
    document.querySelector(`#app-quiz > div > div.test__list > div:nth-child(${index + 1}) > div.test-item__answers > div > div:nth-child(${answer + 1}) > label > span`).click()
}
