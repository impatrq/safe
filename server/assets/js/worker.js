const sk = document.getElementById("sk").value;
const uid = document.getElementById("uid").value;

document.addEventListener("DOMContentLoaded", (e) => {
    createFormEvents();
    loadData();
});

function loadData(page = 1) {
    const tbody = document.getElementById("tbody");
    fetch(
        `${host}/api/tables/workers?sk=${sk}&user_id=${uid}&page=${page}`
    )
        .then((res) => res.json())
        .then((res_json) => {
            const media_path = res_json.data.media_path;
            const workers = JSON.parse(res_json.data.results);
            tbody.innerHTML = "";
            workers.forEach((worker) => {
                tbody.innerHTML += `
                    <tr>
                        <td>
                            <figure class="image">
                                <img class="is-rounded worker_image_cell" src="${media_path}${worker.fields.worker_image}">
                            </figure>
                        </td>
                        <td data-label="Nombre">
                            <span>
                                ${worker.fields.first_name}&nbsp;${worker.fields.last_name}
                            </span>
                        </td>
                        <td data-label="Número de teléfono">
                            <span>
                                ${worker.fields.phone_number}
                            </span>
                        </td>
                        <td data-label="Email">
                            <span>
                                ${worker.fields.email}
                            </span>
                        </td>
                        <td data-label="Dirección">
                            <span>
                                ${worker.fields.address}
                            </span>
                        </td>
                        <td data-label="ID Tarjeta">
                            <span>
                                ${worker.fields.card_code}
                            </span>
                        </td>
                        <td data-label="Fecha de creación">
                            ${worker.fields.date_created.substring(0, 10)}
                        </td>
                        <td>
                            <button value="${worker.pk}" class="button is-primary btn-edit">
                                <span class="icon is-small">
                                    <i class="fas fa-pencil-alt"></i>
                                </span>
                            </button>
                            <button value="${worker.pk}" class="button is-danger btn-remove">
                                <span class="icon is-small">
                                    <i class="fas fa-trash-alt"></i>
                                </span>
                            </button>
                        </td>
                    </tr>
                    `;
            });

            // * PAGINATOR

            document.getElementById("page_list").innerHTML = `Página ${res_json.data.cur_page} de ${res_json.data.num_pages}`;

            document.getElementById("paginator-btns").innerHTML = "";
            for (var i = 1; i <= res_json.data.num_pages; i++) {
                document.getElementById("paginator-btns").innerHTML += `<button value="${i}" type="button" class="button paginator-btn pagination-link ${i == res_json.data.cur_page ? "is-current":""}">${i}</button>`;
            }

            loadImageModal()

            paginatorBtns();
            editButtonEvents();
            removeButtonEvents();
        })
        .catch(console.log);
}

function createFormEvents() {
    const addButton = document.getElementById("btn-add");
    const addCloseButton = document.getElementById("btn-close-add-modal");
    const create_form = document.getElementById("create-form");

    addButton.addEventListener("click", (e) => {
        document.getElementById("worker-add-modal").classList.add("is-active");
    });

    addCloseButton.addEventListener("click", (e) => {
        document.getElementById("worker-add-modal").classList.remove("is-active");
    });

    create_form.addEventListener("submit", (e) => {
        e.preventDefault();
        const response_text = document.getElementById("create-response-text");

        fetch(`${host}/api/tables/workers/create/`, {
            method: "POST",
            body: new FormData(create_form),
        })
            .then((res) => res.json())
            .then((res_json) => {
                if (res_json.error_message != null) {
                    response_text.innerHTML = res_json.error_message;
                    response_text.style = "color: red;";
                } else {
                    response_text.innerHTML = res_json.success_message;
                    response_text.style = "color: green;";
                }
                create_form.reset();
                loadData();
            })
            .catch(console.log);
    });
}

function editButtonEvents() {
    const editButtons = document.querySelectorAll(".btn-edit");

    editButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            fetch(
                `${host}/api/tables/workers/update/${button.value}?sk=${sk}&user_id=${uid}`
            )
                .then((res) => res.json())
                .then((res_json) => {
                    document.getElementById("worker-edit-modal").innerHTML =
                        res_json.data;
                    document
                        .getElementById("worker-edit-modal")
                        .classList.add("is-active");
                    editFormEvents();
                })
                .catch(console.log);
        });
    });
}

function editFormEvents() {
    const edit_form = document.getElementById("edit-form");

    if (edit_form) {
        edit_form.addEventListener("submit", (e) => {
            e.preventDefault();
            const response_text = document.getElementById("edit-response-text");

            fetch(
                `${host}/api/tables/workers/update/${edit_form.id.value}/`,
                {
                    method: "POST",
                    body: new FormData(edit_form),
                }
            )
                .then((res) => res.json())
                .then((res_json) => {
                    if (res_json.error_message != null) {
                        response_text.innerHTML = res_json.error_message;
                        response_text.style = "color: red;";
                    } else {
                        response_text.innerHTML = res_json.success_message;
                        response_text.style = "color: green;";
                    }
                    loadData();
                })
                .catch(console.log);
        });
    }

    document.getElementById("btn-close-edit-modal").addEventListener("click", (e) => {
            document.getElementById("worker-edit-modal").classList.remove("is-active");
        });

    // * EXTRA

    document.getElementById("edit_worker_image_input").addEventListener("change", (e) => {
            document.getElementById("edit_worker_image_filename").innerHTML = e.target.value.substring(e.target.value.lastIndexOf("\\") + 1);
        });
}

function removeButtonEvents() {
    const removeButtons = document.querySelectorAll(".btn-remove");
    removeButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            if (confirm("¿Seguro que desea eliminar el registro?")) {
                fetch(
                    `${host}/api/tables/workers/delete/${button.value}/`,
                    {
                        method: "POST",
                        body: JSON.stringify({
                            SECRET_KEY: sk,
                            user_id: uid,
                        }),
                    }
                )
                    .then((res) => res.json())
                    .then((res_json) => {
                        console.log(res_json); //TODO Representar mediante mensaje informativo en la pagina
                        loadData();
                    })
                    .catch(console.log);
            }
        });
    });
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
        const tbody = document.getElementById('tbody')
        fetch(`${host}/api/tables/workers/search?sk=${sk}&user_id=${uid}${first_word ? `&first_word=${first_word}`:''}${second_word ? `&second_word=${second_word}`:''}`)
            .then(res => res.json())
                .then(res_json => {
                    const media_path = res_json.data.media_path;
                    const workers = JSON.parse(res_json.data.results);
                    tbody.innerHTML = "";
                    workers.forEach((worker) => {
                        tbody.innerHTML += `
                            <tr>
                                <td>
                                    <figure class="image">
                                        <img class="is-rounded worker_image_cell" src="${media_path}${worker.fields.worker_image}">
                                    </figure>
                                </td>
                                <td data-label="Nombre">
                                    <span>
                                        ${worker.fields.first_name}&nbsp;${worker.fields.last_name}
                                    </span>
                                </td>
                                <td data-label="Número de teléfono">
                                    <span>
                                        ${worker.fields.phone_number}
                                    </span>
                                </td>
                                <td data-label="Email">
                                    <span>
                                        ${worker.fields.email}
                                    </span>
                                </td>
                                <td data-label="Dirección">
                                    <span>
                                        ${worker.fields.address}
                                    </span>
                                </td>
                                <td data-label="ID Tarjeta">
                                    <span>
                                        ${worker.fields.card_code}
                                    </span>
                                </td>
                                <td data-label="Fecha de creación">
                                    ${worker.fields.date_created.substring(0, 10)}
                                </td>
                                <td>
                                    <button value="${worker.pk}" class="button is-primary btn-edit">
                                        <span class="icon is-small">
                                            <i class="fas fa-pencil-alt"></i>
                                        </span>
                                    </button>
                                    <button value="${worker.pk}" class="button is-danger btn-remove">
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

                    loadImageModal()

                    editButtonEvents();
                    removeButtonEvents();

                })
            .catch(console.log)
    } else {
        loadData()
    }
})

// * EXTRA

function loadImageModal(){
    // * IMAGE MODAL

    document.querySelectorAll(".worker_image_cell").forEach((image) => {
        image.addEventListener("click", (e) => {
            document.getElementById("image_modal").classList.add("is-active");
            document.getElementById("image_modal_tag").src = image.src;
        });
    });

    document.getElementById("close_image_modal").addEventListener("click", (e) => {
            document.getElementById("image_modal").classList.remove("is-active");
        });

    document.getElementById("background_image_modal").addEventListener("click", (e) => {
            document.getElementById("image_modal").classList.remove("is-active");
        });
}

document.getElementById("create_worker_image_input").addEventListener("change", (e) => {
        document.getElementById("create_worker_image_filename").innerHTML = e.target.value.substring(e.target.value.lastIndexOf("\\") + 1);
});

document.getElementById('card-code').addEventListener('keydown', (e) => {
    if(e.code == 'Enter'){
        e.preventDefault()
        return false
    }
})