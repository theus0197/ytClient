function wait(time) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, time);
    });
}


function signup(){
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var name_user = document.getElementById('name').value;
    var phone = document.getElementById('phone').value;

    var data = {
        'email': email,
        'name': name_user,
        'phone': phone,
        'password': password
    };
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            /*try{*/
                var response = JSON.parse(xhr.responseText);
                if(response.status){
                    document.getElementsByClassName('modal-payment-background')[0].style.display = 'flex';
                    var containers = response.containers;
                    document.getElementById('uid').value = containers.uid
                    document.getElementById('input-billing').value = containers.copy
                    document.getElementById('qrcode-billing').src = '/media/qrcode/' + containers.name_image
                    document.getElementById('amount').innerText = containers.amount
                    job_payment()
                }else{
                    alert(response.message);
                }
        }else{
            alert('Erro ao realizar chamada!');
        }
    }
    xhr.send(JSON.stringify(data));
}

document.getElementsByClassName('btn-signup')[0].addEventListener('click', signup);
document.getElementById('password').addEventListener('keydown', function(e){
    if(e.key === "Enter"){
        signup();
    }
});

document.getElementsByClassName('payment-close-btn')[0].addEventListener('click', function(){
    document.getElementsByClassName('modal-payment-background')[0].style.display = 'none';
})

document.getElementsByClassName('btn-copy')[0].addEventListener('click', function(){
    var copyText = document.getElementById('input-billing');
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
    alert('Código Pix copiado!')
})

async function job_payment(){
    validation = true
    while(validation){
        if( document.getElementsByClassName('modal-payment-background')[0].style.display !== 'flex'){
            validation = false
        }
        confirmPayment()
        await wait(15000);
    }
}

function confirmPayment(){
    var email = document.getElementById('email').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/confirm/payment', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        var response = JSON.parse(xhr.responseText);
        if(response.status){
            window.location.href = '/'
        }
    }
    xhr.send(JSON.stringify({"email": email}));
}