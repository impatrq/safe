const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

document.addEventListener('DOMContentLoaded', (e) => {
    loadData()
})

function loadData(page = 1){
    const tbody = document.getElementById('tbody')
    fetch(`http://localhost:8000/api/tables/logs?sk=${sk}&user_id=${uid}&page=${page}`)
        .then(res => res.json())
            .then(res_json => {
                console.log(res_json);
                const media_path = res_json.data.media_path 
                const logs = JSON.parse(res_json.data.results)
                console.log(logs);
                tbody.innerHTML = ''
                logs.forEach(log => {
                    tbody.innerHTML += `
                    <tr>
                        <td>
                            <figure class="image">
                                <img class="is-rounded worker_image_cell" src="${media_path}${log.worker_image.substring(7)}">
                            </figure>
                        </td>
                        <td data-label="Nombre">${log.worker_full_name}</td>
                        <td data-label="Puerta">${log.door_name}</td>
                        <!-- <td data-label="Sector">Oficinas</td> -->
                        <td data-label="Temperatura">${log.temperature}°c</td>
                        <td data-label="Barbijo">${log.facemask == true ? "Si":"No"}</td>
                        <td data-label="Hora de entrada">${formatDateTime(log.entry_datetime)}</td>
                        <td data-label="Hora de salida">${formatDateTime(log.exit_datetime)}</td>
                        <td data-label="Autorizado">
                            <span class="icon ${log.authorized == true ? 'has-text-success':'has-text-danger'}">
                                <i class="far ${log.authorized == true ? 'fa-check-circle':'fa-times-circle'}"></i>
                            </span>
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

                loadImageModal()
                paginatorBtns()

            })
        .catch(console.log)
}

function formatDateTime(datetime){

    if(datetime != '-'){
        var date = datetime.substring(0, 10).split('-')
        const time = datetime.substring(11,19)
        
        const y = date[0]
        const m = date[1]
        const d = date[2]

        return `${m}/${d}/${y} a las ${time}`
    } else {
        return '-'
    }
    
}

function formatDateMilis(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

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

function paginatorBtns() {
    const paginator_btns = document.querySelectorAll(".paginator-btn");
    paginator_btns.forEach((button) => {
        button.addEventListener("click", (e) => {
            loadData(e.target.value);
        });
    });
}

// * SEARCH BAR

document.getElementById('search-btn').addEventListener('click', (e) => {
    const search_bar = document.getElementById('search-bar').value
    const first_word = search_bar.split(' ')[0]
    const second_word = search_bar.split(' ')[1]

    var from_search_date = document.getElementById('from_search_date').value
    var from_search_time = document.getElementById('from_search_time').value

    var to_search_date = document.getElementById('to_search_date').value
    var to_search_time = document.getElementById('to_search_time').value

    if(to_search_date == '' && from_search_date != ''){
        // to_search_date = formatDateMilis(Date.now())
        to_search_date = 'null'
    }

    if(from_search_date == '' && to_search_date != ''){
        // from_search_date = '2000-01-01'
        from_search_date = 'null'
    }

    if(to_search_time == '' && from_search_time != ''){
        to_search_time = '23:59'
        // to_search_time = 'none'
    }
    
    if(from_search_time == '' && to_search_time != ''){
        from_search_time = '00:00'
        // from_search_time = 'none'
    }

    if(search_bar || from_search_date){
        const tbody = document.getElementById('tbody')
        fetch(`http://localhost:8000/api/tables/logs/search?sk=${sk}&user_id=${uid}${first_word ? `&first_word=${first_word}`:''}${second_word ? `&second_word=${second_word}`:''}${from_search_date ? `&from_search_date=${from_search_date}`:''}${from_search_time ? `&from_search_time=${from_search_time}`:''}${to_search_date ? `&to_search_date=${to_search_date}`:''}${to_search_time ? `&to_search_time=${to_search_time}`:''}`)
            .then(res => res.json())
                .then(res_json => {
                    console.log(res_json);
                    const media_path = res_json.data.media_path 
                    const logs = JSON.parse(res_json.data.results)
                    console.log(logs);
                    tbody.innerHTML = ''
                    logs.forEach(log => {
                        tbody.innerHTML += `
                        <tr>
                            <td>
                                <figure class="image">
                                    <img class="is-rounded worker_image_cell" src="${media_path}${log.worker_image.substring(7)}">
                                </figure>
                            </td>
                            <td data-label="Nombre">${log.worker_full_name}</td>
                            <td data-label="Puerta">${log.door_name}</td>
                            <!-- <td data-label="Sector">Oficinas</td> -->
                            <td data-label="Temperatura">${log.temperature}°c</td>
                            <td data-label="Barbijo">${log.facemask == true ? "Si":"No"}</td>
                            <td data-label="Hora de entrada">${formatDateTime(log.entry_datetime)}</td>
                            <td data-label="Hora de salida">${formatDateTime(log.exit_datetime)}</td>
                            <td data-label="Autorizado">
                                <span class="icon ${log.authorized == true ? 'has-text-success':'has-text-danger'}">
                                    <i class="far ${log.authorized == true ? 'fa-check-circle':'fa-times-circle'}"></i>
                                </span>
                            </td>
                        </tr>
                        `
                    })

                    // * PAGINATOR

                    document.getElementById("page_list").innerHTML = "";
                    document.getElementById("paginator-btns").innerHTML = "";

                    loadImageModal()

                })
            .catch(console.log)
    } else {
        loadData()
    }

})

document.getElementById('reset-btn').addEventListener('click', (e) => {
    document.getElementById('search-bar').value = ''

    document.getElementById('from_search_date').value = ''
    document.getElementById('from_search_time').value = ''

    document.getElementById('to_search_date').value = ''
    document.getElementById('to_search_time').value = ''

    loadData()

})