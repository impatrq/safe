const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

var doorsTimer = setInterval(updateCards, 30000)

document.addEventListener('DOMContentLoaded', (e) => {
    loadCards()
})

function loadCards(){
        fetch(`http://localhost:8000/api/tables/doors?sk=${sk}&user_id=${uid}`)
            .then(res => res.json())
                .then(res_json => {

                        // <div class="card" id="card" style="display: inline-block; padding: 100px; background-color: #333; color: #f2f2f2;">
                        //     <input type="hidden" class="id" name="id" value="${door.pk}">
                        //     <p>Door: </p>
                        //     <p>Is Opened: <span id="is_opened">${door.fields.is_opened}</span></p>
                        //     <p>Sanitizer: <span id="sanitizer_perc">${door.fields.sanitizer_perc}</span></p>
                        // </div>

                    doors = JSON.parse(res_json.data.results)
                    document.getElementById('doors-container').innerHTML = ''
                    doors.forEach(door => {
                        document.getElementById('doors-container').innerHTML += `
                        <div class="column is-4">
                            <div class="card get_logs log_button" id="${door.pk}">
                                <div class="card-content has-text-centered">
                                    <div class="level is-mobile">
                                        <div class="level-item">
                                            <div class="is-widget-label">
                                            <h3 class="subtitle is-spaced">${door.fields.sector_name} - ${door.fields.door_name}</h3>
                                            <h1 class="title is-opened-flag">${door.fields.is_opened == true ? "Abierta":"Cerrada"}</h1>
                                            <h1>Sanitizante: <span>${door.fields.sanitizer_perc}</span></h1>
                                            <input type="hidden" name="id" value="${door.pk}">
                                            </div>
                                        </div>
                                        <div class="level-item has-widget-icon">
                                            <div class="is-widget-icon">
                                                <span class="icon has-text-primary is-large"><i class="mdi mdi-door-open mdi-48px"></i></span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        `
                    })
                    loadBtns()
                })
            .catch(console.log)
}

async function updateCards(){

    const flags = document.querySelectorAll('.is-opened-flag')

    const doors = undefined
    
    await fetch(`http://localhost:8000/api/tables/doors/get_doors_status?sk=${sk}&user_id=${uid}`)
            .then(res => res.json())
                .then(res_json => {
                    this.doors = JSON.parse(res_json.data)
                })
            .catch(console.log)

    flags.forEach(flag => {
        const door = this.doors[flag.nextElementSibling.nextElementSibling.value]
        flag.innerHTML = door.is_opened == true ? "Abierta":"Cerrada"
        flag.nextElementSibling.firstElementChild.innerHTML = door.sanitizer_perc
    })
}

async function get_door_info(id){
    
    return await fetch(`http://localhost:8000/api/tables/doors/get_doors_status?sk=${sk}&user_id=${uid}`)
        .then(res => res.json())
            .then(res_json => {
                const data = JSON.parse(res_json.data)[id]
                const last_logs = JSON.parse(data.last_logs)
                const people_inside = JSON.parse(data.people_inside)
                return {
                    last_logs: last_logs,
                    people_inside: people_inside,
                    is_opened: data.is_opened,
                    sanitizer_perc: data.sanitizer_perc,
                    door_name: data.door_name,
                    is_safe: data.is_safe,
                    // co2_level: data.co2_level,
                }
            })
        .catch(console.log)
}

function loadBtns(){
    const logs_btns = document.querySelectorAll('.get_logs')
    const log_list = document.getElementById('logs_list')

    logs_btns.forEach(button => {
        button.addEventListener('click', async (e) => {
            const door_info = await get_door_info(button.id)
            
            document.getElementById('modal-log').classList.add('is-active')

            document.getElementById('people_inside').innerHTML = door_info.people_inside.length

            document.getElementById('sanitizer_perc').innerHTML = door_info.sanitizer_perc

            document.getElementById('door-title').innerHTML = door_info.door_name

            document.getElementById('is_safe').innerHTML = door_info.is_safe == true ? "Si":"No"

            log_list.innerHTML = ""
            door_info.last_logs.forEach(log => {
                log_list.innerHTML += `
                    <tr>
                        <td class="is-image-cell">
                            <div class="image">
                            <img src="${log.worker_image}" class="is-rounded" />
                            </div>
                        </td>
                        <td data-label="Nombre">${log.worker_full_name}</td>
                        <td data-label="Temperatura">${log.temperature}°c</td>
                        <td data-label="Barbijo">${log.facemask == true ? "Si":"No"}</td>
                        <td data-label="Hora de entrada">${log.entry_datetime}</td>
                        <td data-label="Hora de salida">${log.exit_datetime}</td>
                        <td data-label="Autorizado">
                            <span class="icon has-text-success">
                                <i class="far ${log.authorized == true ? "fa-check-circle":"fa-times-circle has-text-danger"}"></i>
                            </span>
                        </td>
                    </tr>

                `
            })

        })
    })

    document.getElementById('modal-log-close').addEventListener('click', (e) => {
        document.getElementById('modal-log').classList.remove('is-active')
    })

}

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

    fetch('http://localhost:8000/api/tables/report/', {
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