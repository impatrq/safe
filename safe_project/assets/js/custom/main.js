const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

var doorsTimer = setInterval(updateCards, 5000)

document.addEventListener('DOMContentLoaded', (e) => {
    loadCards()
})

function loadCards(){
        fetch(`http://localhost:8000/api/tables/doors?sk=${sk}&user_id=${uid}`)
            .then(res => res.json())
                .then(res_json => {

                    doors = JSON.parse(res_json.data.results)
                    document.getElementById('doors-container').innerHTML = ''
                    doors.forEach(door => {
                        document.getElementById('doors-container').innerHTML += `
                        <div class="card" id="card" style="display: inline-block; padding: 100px; background-color: #333; color: #f2f2f2;">
                            <input type="hidden" class="id" name="id" value="${door.pk}">
                            <p>Door: ${door.fields.sector_name} - ${door.fields.door_name}</p>
                            <p>Is Opened: <span id="is_opened">${door.fields.is_opened}</span></p>
                            <p>Sanitizer: <span id="sanitizer_perc">${door.fields.sanitizer_perc}</span></p>
                        </div>
                        `
                    })

                })
            .catch(console.log)
}

async function updateCards(){

    const cards = document.querySelectorAll('.card')

    const doors = undefined
    
    await fetch(`http://localhost:8000/api/tables/doors/get_doors_status?sk=${sk}&user_id=${uid}`)
            .then(res => res.json())
                .then(res_json => {
                    this.doors = JSON.parse(res_json.data)
                })
            .catch(console.log)

    cards.forEach(card => {
        const door = this.doors[card.firstElementChild.value]
        card.children[2].firstElementChild.innerHTML = door.is_opened
        card.children[3].firstElementChild.innerHTML = door.sanitizer_perc
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
                }
            })
        .catch(console.log)
}

const logs_btns = document.querySelectorAll('.get_logs')
const people_inside_div = document.getElementById('people_inside')
const log_list_div = document.getElementById('logs_list')

logs_btns.forEach(button => {
    button.addEventListener('click', async (e) => {
        const door_info = await get_door_info(e.target.value)
        
        door_info.people_inside.forEach(person => {
            people_inside_div.innerHTML += `${person.fields.first_name} ${person.fields.last_name} | `
        })

        door_info.last_logs.forEach(log => {
            log_list_div.innerHTML += `
                <div style="padding: 50px; background-color: #333; color: #f2f2f2; display: inline-block; margin: 30px">
                    <img src="${log.worker_image}" alt="Image" width="50px" height="50px">
                    <p>Worker Name: ${log.worker_full_name}</p>
                    <p>Entry Datetime: ${log.entry_datetime}</p>
                    <p>Exit Datetime: ${log.exit_datetime}</p>
                    <p>Authorized: ${log.authorized}</p>
                    <p>Facemask: ${log.facemask}</p>
                    <p>Temperature: ${log.temperature}</p>
                    <p>Sector Name: ${log.sector_name}</p>
                    <p>Door Name: ${log.door_name}</p>
                </div>
            `
        })

    })
})