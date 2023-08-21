function confirmForms(){    
    anwser = document.getElementsByClassName('answer-1')[0].value;
    if(anwser === 'yes' || anwser === 'no'){
        anwser = document.getElementsByClassName('answer-2')[0].value;
        if(anwser === 'yes' || anwser === 'no'){
            anwser = document.getElementsByClassName('answer-3')[0].value;
            if(anwser === 'yes' || anwser === 'no'){
                var data = {
                    'answer_1': document.getElementsByClassName('answer-1')[0].value,
                    'answer_2': document.getElementsByClassName('answer-2')[0].value,
                    'answer_3': document.getElementsByClassName('answer-3')[0].value,
                    'enterprise': document.getElementById('enterprise-name').value
                };
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/api/confirm/forms', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        if(response.status){
                            window.location.href = '/';
                        }else{
                            //alert(response.message);
                            document.getElementsByClassName('modal-alerts')[0].style.display  = 'flex';
                            document.getElementsByClassName('status-report')[0].textContent  = response.message;

                        }
                    } else {
                        alert('Erro ao realizar chamada!');
                    }
                }
                xhr.send(JSON.stringify(data));
            }else{
                document.getElementsByClassName('modal-alerts')[0].style.display  = 'flex';
                document.getElementsByClassName('status-report')[0].textContent  = 'Responda a pergunta n° 3';
            }
        }else{
            document.getElementsByClassName('modal-alerts')[0].style.display  = 'flex';
            document.getElementsByClassName('status-report')[0].textContent  = 'Responda a pergunta n° 2';
        }
    }else{
        document.getElementsByClassName('modal-alerts')[0].style.display  = 'flex';
        document.getElementsByClassName('status-report')[0].textContent = 'Responda a pergunta n° 1';
    }
    
    
}
document.getElementsByClassName("confirm-form")[0].addEventListener("click", confirmForms);
document.getElementsByClassName("modal-close-alerts")[0].addEventListener("click", function(){
    document.getElementsByClassName('modal-alerts')[0].style.display = 'none'
});
