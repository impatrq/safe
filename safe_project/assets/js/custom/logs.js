const sk = document.getElementById('sk').value
const uid = document.getElementById('uid').value

document.addEventListener('DOMContentLoaded', (e) => {
    loadData()
})

function loadData(){
    const tbody = document.getElementById('tbody')
    fetch(`http://localhost:8000/api/tables/logs?sk=${sk}&user_id=${uid}`)
        .then(res => res.json())
            .then(res_json => {
                // console.log(res_json);
                const media_path = res_json.data.media_path 
                const logs = JSON.parse(res_json.data.results)
                console.log(logs);
                tbody.innerHTML = ''
                logs.forEach(log => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${log.worker_full_name}</td>
                        <td>${log.door_name}</td>
                        <td>${log.facemask}</td>
                        <td>${log.temperature}</td>
                        <td>${log.authorized}</td>
                        <td>${log.entry_datetime}</td>
                        <td>${log.exit_datetime}</td>
                        <td><img src="${media_path}${log.worker_image.substring(7)}" alt="" height="50px" width="50px"></td>
                    </tr>
                    `
                })
            })
        .catch(console.log)
}