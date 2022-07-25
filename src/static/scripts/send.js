function post_form() {
    xhr = new XMLHttpRequest()
    xhr.open("POST", window.location.pathname.split('/').slice(-1)[0])
    xhr.onload = () => {
        if (xhr.status === 201) {
            alert('Заявка подана')
        }
    }
    data = {
        lastname: document.getElementById('last').value,
        firstname: document.getElementById('first').value,
        middlename: document.getElementById('middle').value,
        wonder_nick: document.getElementById('nick').value,
        wonder_role: document.getElementById('roles').value,
        religion: document.getElementById('religion').value,
        nation: document.getElementById('nation').value,
        sex: document.getElementById('sex').value,
        birth_date: new Date(document.getElementById('birth_date').value).getTime()
    }
    xhr.send(JSON.stringify(data))
}