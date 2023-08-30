function login(){
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var data = {
        'email': email,
        'password': password
    };
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            try{
                var response = JSON.parse(xhr.responseText);
                if(response.status){
                    window.location.href = '/';
                }else{
                    alert(response.message);
                }
            }catch(e){
                var response_html = xhr.responseText;
                var alerts = document.getElementsByClassName('modal-alerts-center')[0];
                alerts.innerHTML = response_html;
                document.getElementsByClassName('modal-alerts')[0].style.display = 'flex';
                var close_alert = document.getElementsByClassName('close-notification')[0]
                close_alert.addEventListener('click', function(){
                    document.getElementsByClassName('modal-alerts')[0].style.display = 'none';
                })
                

            }
        } else {
            alert('Error when making call!');
        }
    }
    xhr.send(JSON.stringify(data));
}

document.getElementsByClassName('btn-signin')[0].addEventListener('click', login);
document.getElementById('password').addEventListener('keydown', function(e){
    if(e.key === "Enter"){
        login();
    }
});