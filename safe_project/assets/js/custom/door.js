const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

document.addEventListener('DOMContentLoaded', (e) => {
    loadData()
})

function loadData(){
    const tbody = document.getElementById('tbody')
    fetch(`http://localhost:8000/api/tables/doors?sk=${sk}&user_id=${uid}`)
        .then(res => res.json())
            .then(res_json => {
                const doors = JSON.parse(res_json.data.results)
                tbody.innerHTML = ''
                doors.forEach(door => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${door.fields.sector_name}</td>
                        <td>${door.fields.door_name}</td>
                        <td>${door.fields.is_opened}</td>
                        <td>${door.fields.sanitizer_perc}</td>
                        <td>${door.fields.is_active}</td>
                        <td><button value="${door.pk}" class="btn-edit">Edit</button></td>
                        <td><button value="${door.pk}" class="btn-remove">Remove</button></td>
                    </tr>
                    `
                })
                editButtonEvents()
                removeButtonEvents()
            })
        .catch(console.log)
}

function editButtonEvents(){
    const editButtons = document.querySelectorAll('.btn-edit')
    const editDiv = document.getElementById('edit-div')
    
    editButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            fetch(`http://localhost:8000/api/tables/doors/update/${e.target.value}?sk=${sk}&user_id=${uid}`)
                .then(res => res.json())
                    .then(res_json => {
                        editDiv.innerHTML = res_json.data
                        editDiv.style.display = 'block'
                        editFormEvents()
                    })
                .catch(console.log)
        })
    })
}

function editFormEvents(){
    
    const edit_form = document.getElementById('edit-form')

    if(edit_form){
        edit_form.addEventListener('submit', (e) => {
            e.preventDefault()
    
            fetch(`http://localhost:8000/api/tables/doors/update/${edit_form.id.value}/`, {
                method: 'POST',
                body: new FormData(edit_form),
            })
                .then(res => res.json())
                    .then(res_json => {
                        console.log(res_json) //TODO Representar mediante mensaje informativo en la pagina
                        loadData()
                    })
                .catch(console.log)
        })    
    }
}

function removeButtonEvents(){
    const removeButtons = document.querySelectorAll('.btn-remove')
    removeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            fetch(`http://localhost:8000/api/tables/doors/delete/${e.target.value}/`, {
                method: 'POST',
                body: JSON.stringify({
                    SECRET_KEY: sk,
                    user_id: uid
                })
            })
                .then(res => res.json())
                    .then(res_json => {
                        console.log(res_json) //TODO Representar mediante mensaje informativo en la pagina
                        loadData()
                    })
                .catch(console.log)
        })
    })

}