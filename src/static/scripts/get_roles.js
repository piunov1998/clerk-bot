let list = document.getElementById('roles')
xhr = new XMLHttpRequest()
xhr.responseType = 'json'
xhr.open("GET", "../bot/api/roles")

xhr.onload = () => {

    if (xhr.status === 200) {
        let roles = xhr.response
        for (role of roles) {
            opt = document.createElement('option')
            opt.value = role.id
            opt.innerText = role.name
            list.appendChild(opt)
        }
    }
}
xhr.send()