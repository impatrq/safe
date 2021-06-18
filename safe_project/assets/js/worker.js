const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

document.addEventListener('DOMContentLoaded', (e) => {
    createFormEvents()
    loadData()
})

function loadData(){
    const tbody = document.getElementById('tbody')
    fetch(`http://localhost:8000/api/tables/workers?sk=${sk}&user_id=${uid}`)
        .then(res => res.json())
            .then(res_json => {
                const media_path = res_json.data.media_path 
                const workers = JSON.parse(res_json.data.results)
                tbody.innerHTML = ''
                workers.forEach(worker => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${worker.fields.first_name}</td>
                        <td>${worker.fields.last_name}</td>
                        <td>${worker.fields.phone_number}</td>
                        <td>${worker.fields.email}</td>
                        <td>${worker.fields.address}</td>
                        <td>${worker.fields.card_code}</td>
                        <td><img src="${media_path}${worker.fields.worker_image}" alt="" height="50px" width="50px"></td>
                        <td>${worker.fields.is_active}</td>
                        <td><button value="${worker.pk}" class="btn-edit">Edit</button></td>
                        <td><button value="${worker.pk}" class="btn-remove">Remove</button></td>
                    </tr>
                    `
                })
                editButtonEvents()
                removeButtonEvents()
            })
        .catch(console.log)
}

function createFormEvents(){
    const addButton = document.getElementById('btn-add')
    const createDiv = document.getElementById('create-div')
    const create_form = document.getElementById('create-form')

    addButton.addEventListener('click', (e) => {
        createDiv.style.display = 'block'
    })
    
    create_form.addEventListener('submit', (e) => {
        e.preventDefault()
    
        fetch('http://localhost:8000/api/tables/workers/create/', {
            method: 'POST',
            body: new FormData(create_form),
        })
            .then(res => res.json())
                .then(res_json => {
                    console.log(res_json) //TODO Representar mediante mensaje informativo en la pagina 
                    loadData()
                })
            .catch(console.log)
    
    })
}

function editButtonEvents(){
    const editButtons = document.querySelectorAll('.btn-edit')
    const editDiv = document.getElementById('edit-div')
    
    editButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            fetch(`http://localhost:8000/api/tables/workers/update/${e.target.value}?sk=${sk}&user_id=${uid}`)
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
    
            fetch(`http://localhost:8000/api/tables/workers/update/${edit_form.id.value}/`, {
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
            fetch(`http://localhost:8000/api/tables/workers/delete/${e.target.value}/`, {
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