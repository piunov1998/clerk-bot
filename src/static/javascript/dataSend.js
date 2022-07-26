function SendData() {
    let firstname = document.getElementById('firstname').value
    let lastname = document.getElementById('lastname').value
    let middlename = document.getElementById('middlename').value
    let nation = document.getElementById('nation').value
    let religion = document.getElementById('religion').value
    let nickname = document.getElementById('nickname').value
    let selectRole = document.getElementById('select-role').value
    let birthday = document.getElementById('birthday').value

    let sex = ''

    for (radioSex of document.getElementsByName('sex')) {
        if (radioSex.checked) {
            sex = radioSex.value
        }
    }

    let allData = {
        firstname: firstname,
        lastname: lastname,
        middlename: middlename,
        nation: nation,
        religion: religion,
        wonder_nick: nickname,
        wonder_role: selectRole,
        sex: sex,
        birth_date: new Date(birthday).getTime()
    }

    let xhr = new XMLHttpRequest();

    xhr.open('POST', window.location.pathname.split('/').slice(-1)[0]);

    xhr.onload = () => {
        if (xhr.status === 201) {
            alert('Заявка отправлена на рассмотрение')
        }
    }

    xhr.send(JSON.stringify(allData))
}
