let list = document.getElementById('select-role')

let xhr = new XMLHttpRequest()

xhr.responseType = 'json'

xhr.open('GET', '../bot/api/roles')

xhr.onload = () => {
    if (xhr.status === 200) {
        let roles = xhr.response
        for (role of roles) {
            let option = document.createElement('option')
            option.value = role.id
            option.innerText = role.name
            list.appendChild(option)
        }
    }
}

xhr.send()
