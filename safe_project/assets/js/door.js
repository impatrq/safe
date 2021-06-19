const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

document.addEventListener('DOMContentLoaded', (e) => {
    loadData()
})

function loadData(page = 1){
    const tbody = document.getElementById('tbody')
    fetch(`http://localhost:8000/api/tables/doors?sk=${sk}&user_id=${uid}&page=${page}`)
        .then(res => res.json())
            .then(res_json => {
                const doors = JSON.parse(res_json.data.results)
                tbody.innerHTML = ''
                doors.forEach(door => {
                    tbody.innerHTML += `
                    <tr>
                        <td data-label="Sector">
                            <span>
                                ${door.fields.sector_name}
                            </span>
                        </td>
                        <td data-label="Puerta">
                            <span>
                                ${door.fields.door_name}
                            </span>
                        </td>
                        <td data-label="Esta abierta">
                            <span>
                                ${door.fields.is_opened == true ? "Si":"No"}
                            </span>
                        </td>
                        <td data-label="Sanitizante">
                            <span>
                                ${door.fields.sanitizer_perc}
                            </span>
                        </td>
                        <td data-label="Fecha de creación">
                            <span>
                                ${door.fields.date_created.substring(0,10)}
                            </span>
                        </td>
                        <td>
                            <button value="${door.pk}" class="button is-primary btn-edit">
                                <span class="icon is-small">
                                    <i class="fas fa-pencil-alt"></i>
                                </span>
                            </button>
                            <button value="${door.pk}" class="button is-danger btn-remove">
                                <span class="icon is-small">
                                    <i class="fas fa-trash-alt"></i>
                                </span>
                            </button>
                        </td>
                    </tr>
                    `
                })

                // * PAGINATOR

                document.getElementById("page_list").innerHTML = `Página ${res_json.data.cur_page} de ${res_json.data.num_pages}`;

                document.getElementById("paginator-btns").innerHTML = "";
                for (var i = 1; i <= res_json.data.num_pages; i++) {
                    document.getElementById("paginator-btns").innerHTML += `<button value="${i}" type="button" class="button paginator-btn pagination-link ${i == res_json.data.cur_page ? "is-current":""}">${i}</button>`;
                }

                paginatorBtns()
                editButtonEvents()
                removeButtonEvents()
            })
        .catch(console.log)
}

function editButtonEvents(){
    const editButtons = document.querySelectorAll('.btn-edit')
    
    editButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            fetch(`http://localhost:8000/api/tables/doors/update/${button.value}?sk=${sk}&user_id=${uid}`)
                .then(res => res.json())
                    .then(res_json => {
                        document.getElementById('door-edit-modal').innerHTML = res_json.data
                        document.getElementById('door-edit-modal').classList.add('is-active')
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
            const response_text = document.getElementById("edit-response-text");
    
            fetch(`http://localhost:8000/api/tables/doors/update/${edit_form.id.value}/`, {
                method: 'POST',
                body: new FormData(edit_form),
            })
                .then(res => res.json())
                    .then(res_json => {
                        if (res_json.error_message != null) {
                            response_text.innerHTML = res_json.error_message;
                            response_text.style = "color: red;";
                        } else {
                            response_text.innerHTML = res_json.success_message;
                            response_text.style = "color: green;";
                        }
                        loadData()
                    })
                .catch(console.log)
        })    
    }

    document.getElementById("btn-close-edit-modal").addEventListener("click", (e) => {
        document.getElementById("door-edit-modal").classList.remove("is-active");
    });

}

function removeButtonEvents(){
    const removeButtons = document.querySelectorAll('.btn-remove')
    removeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if(confirm('¿Seguro que quieres eliminar el registro?')){
                fetch(`http://localhost:8000/api/tables/doors/delete/${button.value}/`, {
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
            }
        })
    })

}

function paginatorBtns() {
    const paginator_btns = document.querySelectorAll(".paginator-btn");
    paginator_btns.forEach((button) => {
        button.addEventListener("click", (e) => {
            loadData(e.target.value);
        });
    });
}

// * SEARCH BAR

document.getElementById('search-bar').addEventListener('keyup', (e) => {
    const first_word = document.getElementById('search-bar').value.split(' ')[0]
    const second_word = document.getElementById('search-bar').value.split(' ')[1]

    if(e.target.value){
        fetch(`http://localhost:8000/api/tables/doors/search?sk=${sk}&user_id=${uid}${first_word ? `&first_word=${first_word}`:''}${second_word ? `&second_word=${second_word}`:''}`)
            .then(res => res.json())
                .then(res_json => {
                    const doors = JSON.parse(res_json.data.results);
                    tbody.innerHTML = "";
                    doors.forEach((door) => {
                        tbody.innerHTML += `
                        <tr>
                            <td data-label="Sector">
                                <span>
                                    ${door.fields.sector_name}
                                </span>
                            </td>
                            <td data-label="Puerta">
                                <span>
                                    ${door.fields.door_name}
                                </span>
                            </td>
                            <td data-label="Esta abierta">
                                <span>
                                    ${door.fields.is_opened == true ? "Si":"No"}
                                </span>
                            </td>
                            <td data-label="Sanitizante">
                                <span>
                                    ${door.fields.sanitizer_perc}
                                </span>
                            </td>
                            <td data-label="Fecha de creación">
                                <span>
                                    ${door.fields.date_created.substring(0,10)}
                                </span>
                            </td>
                            <td>
                                <button value="${door.pk}" class="button is-primary btn-edit">
                                    <span class="icon is-small">
                                        <i class="fas fa-pencil-alt"></i>
                                    </span>
                                </button>
                                <button value="${door.pk}" class="button is-danger btn-remove">
                                    <span class="icon is-small">
                                        <i class="fas fa-trash-alt"></i>
                                    </span>
                                </button>
                            </td>
                        </tr>
                            `;
                    });

                    // * PAGINATOR

                    document.getElementById("page_list").innerHTML = "";
                    document.getElementById("paginator-btns").innerHTML = "";

                    editButtonEvents()
                    removeButtonEvents()

                })
            .catch(console.log)
    } else {
        loadData()
    }
})