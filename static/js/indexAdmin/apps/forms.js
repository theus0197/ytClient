document.getElementById('image-profile').addEventListener('click', function() {
    document.getElementsByClassName('input-logo-image')[0].click();
});

document.getElementsByClassName('input-logo-image')[0].addEventListener('change', function() {
    var input = this;
    if(input.files && input.files[0]) {
        var url = URL.createObjectURL(this.files[0]);
        document.getElementById('image-profile').src = url;
    }else{
        url = document.getElementById('image-profile').src;
    };
});
function validateInfo(){
    value = document.getElementsByName('enterprise')[0].value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/panel/api/enterprise/validate/info', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var statusInput = document.getElementsByClassName('status-enterprise')[0];
            if(data.containers.validation){
                statusInput.classList.add('green');
                statusInput.classList.remove('red')
            }else{
                document.getElementById('image-profile').src = data.containers.logo
                statusInput.classList.add('red');
                statusInput.classList.remove('green')
                }
        } else {
            alert('Erro ao realizar chamada!');
        }
    }
    xhr.send(JSON.stringify({
        'value': value
    }));
}

function createEnterprise(){
    if(document.getElementsByClassName('status-enterprise')[0].classList.contains('green')){
        var inputImage = document.getElementsByClassName('input-logo-image')[0]
        if(inputImage.value === '' || inputImage.value === null) {
            var imgContent = ['url', document.getElementById('image-profile').src];
            var name = document.getElementsByName('enterprise')[0].value;
            var xhr = new XMLHttpRequest();
                xhr.open('POST', '/panel/api/enterprise/create', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var data = JSON.parse(xhr.responseText);
                        alert(data.message);
                    } else {
                        alert('Erro ao realizar chamada!');
                    }
                }
                xhr.send(JSON.stringify({'name': name, 'image': imgContent}));
        }else{
            var reader = new FileReader();
            reader.readAsDataURL(inputImage.files[0]);
            reader.onload = function(e) {
                var data = e.target.result;
                var base64 = data.split(',')[1];
                var imgContent = ['base64', base64];
                var name = document.getElementsByName('enterprise')[0].value;
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/panel/api/enterprise/create', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var data = JSON.parse(xhr.responseText);
                        alert(data.message);
                    } else {
                        alert('Erro ao realizar chamada!');
                    }
                }
                xhr.send(JSON.stringify({'name': name, 'image': imgContent}));
            }
        }
    }
}

document.getElementsByClassName('btn-form-create')[0].addEventListener('click', createEnterprise)
document.getElementsByName('enterprise')[0].addEventListener('keyup', validateInfo)