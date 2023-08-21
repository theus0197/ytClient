document.querySelector('#cpf').addEventListener('keypress', function(e) {
    if(e.target.value.length >= 14) {
        alert('CPF inválido');
    }else{
        if(e.target.value !== ''){
            e.target.value = cpf(e.target.value);
        }else{
            e.target.value = '';
        }
    };

});

function cpf(v){
    v=v.replace(/\D/g,"");
    v=v.replace(/(\d{3})(\d)/,"$1.$2");
    v=v.replace(/(\d{3})(\d)/,"$1.$2");
    v=v.replace(/(\d{3})(\d)/,"$1-$2");
    return v;
}

document.querySelector('#payment').addEventListener('keyup', function(e){
    value = document.querySelector('#my-amount').innerText;
    if(e.target.value >= 200){
        if(e.target.value > parseFloat(value)){
            e.target.value = value.replace(',', '.')
        }
    
        pay = e.target.value
        pyour = pay - (pay*0.2);
        pvp = (pay*0.2);

        document.querySelector('#you-pay').innerText = pyour
        document.querySelector('#vp-pay').innerText = pvp
    }else{
        document.querySelector('#you-pay').innerText = '-'
        document.querySelector('#vp-pay').innerText = '-'
    }
})

document.getElementsByClassName('btn-confirm-center')[0].addEventListener('click', function(){
    var cpf = document.getElementById('cpf').value;
    var first_name = document.getElementById('first-name').value;
    var last_name = document.getElementById('last-name').value;
    var amount = document.getElementById('payment').value;
    if(amount >= 200){
        var data = {
            'amount': amount,
            'first_name': first_name,
            'last_name':last_name,
            'cpf':cpf
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/draw', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if(response.status){
                    document.getElementsByClassName('payment-validate')[0].style.display = 'flex';
                    document.getElementById('value-extornado').innerText = response.containers.amount;
                    document.getElementById('pix-code').src = "/media/qrcode/" + response.containers.name_image;
                    document.querySelector('#my-amount').innerText = response.containers.ramount;
                    document.querySelector('#you-pay').innerText = response.containers.youpay;
                }else{
                    alert(response.message);
                }
            }
        }
        xhr.send(JSON.stringify(data));
    }else{
        alert('Mínimo para saque é R$200');
    }
})

