// * REPORTES

document.getElementById('btn-modal-report').addEventListener('click', (e) => {
    document.getElementById('modal-report').classList.add('is-active')
})

document.getElementById('btn-close-modal-report').addEventListener('click', (e) => {
    document.getElementById('modal-report').classList.remove('is-active')
})

const report_personal = document.getElementById('report-personal')
const report_gerencia = document.getElementById('report-gerencia')

document.getElementById('kind-of-report').addEventListener('change', (e) => {
    if(e.target.value == 0){
        report_personal.hidden = true
        report_gerencia.hidden = true
    } else if (e.target.value == 1){
        report_personal.hidden = false
        report_gerencia.hidden = true
    } else {
        report_personal.hidden = true
        report_gerencia.hidden = false
    }
})

document.getElementById('report-form').addEventListener('submit', (e) => {
    e.preventDefault()

    const email = e.target.email.value
    const name = e.target.name.value
    const kor = e.target.kor.options[e.target.kor.selectedIndex].text
    
    const personal_report = e.target.persrep.value == "-" ? null:e.target.persrep.value
    const gerencial_report = e.target.gerrep.value == "-" ? null:e.target.gerrep.value
    
    const message = e.target.message.value
    
    const response_text = document.getElementById('response-text')

    document.getElementById('report-submit-btn').classList.add('is-loading')

    fetch(`${host}/api/tables/report/`, {
        method: 'POST',
        body: JSON.stringify({
            message: `${name} (${email}) tiene un ${kor}: ${personal_report}${gerencial_report}\n${message}`,
            kor: kor
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
            .then(res_json => {
                document.getElementById('report-submit-btn').classList.remove('is-loading')
                if(res_json.error_message != null){
                    response_text.style = "color: red;"
                    response_text.innerHTML = res_json.error_message
                } else {
                    response_text.style = "color: green;"
                    response_text.innerHTML = res_json.success_message
                }
            })
        .catch(console.log)
    
})