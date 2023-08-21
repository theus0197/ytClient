function createUser(){
    var username = document.getElementsByName('username')[0].value;
    var email = document.getElementsByName('email')[0].value;
    var password = document.getElementsByName('password')[0].value;
    var verifyPassword = document.getElementsByName('verify-password')[0].value;
    if(document.getElementsByClassName('status-username')[0].classList.contains('green')){
        if(document.getElementsByClassName('status-email')[0].classList.contains('green')){
            if(document.getElementsByClassName('status-password')[0].classList.contains('green')){
                if(document.getElementsByClassName('status-verify-password')[0].classList.contains('green')){
                    if(password === verifyPassword){
                        var xhr = new XMLHttpRequest();
                        xhr.open('POST', '/panel/api/users/create', true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.onload = function() {
                            if (xhr.status === 200) {
                                var data = JSON.parse(xhr.responseText);
                                alert(data.message);
                                if (data.status) {
                                    loadUsers();
                                } 
                            } else {
                                alert('Erro ao realizar chamada!');
                            }
                        }
                        xhr.send(JSON.stringify({'username': username, 'email': email, 'password': password}));
                    }else{
                        alert('Senhas não conferem!');
                    }
                }
            }
        }
    }
}

function loadUsers(){
    var query = document.getElementsByName('email')[1].value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/panel/api/users', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var containerResults = document.getElementsByClassName('container-results')[0];
            containerResults.innerHTML = xhr.responseText;
            var btnDelete = document.getElementsByClassName('btn-delete');
            for(var i = 0; i < btnDelete.length; i++){
                btnDelete[i].addEventListener('click', function(){
                    var dataId = this.getAttribute('data-id');
                    deleteUser(dataId)
                })
            }

        } else {
            alert('Erro ao realizar chamada!');
        }
    }
    xhr.send(JSON.stringify({'email': query}));
}

function valdiateInfo(key, value){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/panel/api/users/validate/info', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            if (data.status) {
                var statusInput = document.getElementsByClassName('status-' + key)[0];
                if(data.containers.validation){
                    statusInput.classList.add('green');
                    statusInput.classList.remove('red')
                }else{
                    statusInput.classList.add('red');
                    statusInput.classList.remove('green')
                }

            }
        } else {
            alert('Erro ao realizar chamada!');
        }
    }
    xhr.send(JSON.stringify({
        'key': key, 
        'value': value
    }));
}

function deleteUser(username){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/panel/api/users/delete', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            alert(data.message);
            if (data.status) {
                loadUsers();
            } 
        } else {
            alert('Erro ao realizar chamada!');
        }
    }
    xhr.send(JSON.stringify({
        'username': username
    }));
}

document.getElementsByName('email')[1].addEventListener('keyup', loadUsers)
document.getElementsByClassName('btn-form-create')[0].addEventListener('click', createUser)
document.getElementsByName('username')[0].addEventListener('keyup', function(){valdiateInfo('username', this.value)})
document.getElementsByName('email')[0].addEventListener('keyup', function(){valdiateInfo('email', this.value)})
document.getElementsByName('password')[0].addEventListener('keyup', function(){valdiateInfo('password', this.value)})
document.getElementsByName('verify-password')[0].addEventListener('keyup', function(){
    value = this.value;
    password = document.getElementsByName('password')[0].value;
    var statusInput = document.getElementsByClassName('status-verify-password')[0];
    if(value == password){
        statusInput.classList.add('green');
        statusInput.classList.remove('red')
    }else{
        statusInput.classList.add('red');
        statusInput.classList.remove('green')
    }
})
loadUsers()
