document.querySelector('#phone').addEventListener('keypress', function(e) {
    e.target.value = phone(e.target.value);
});

function phone(v){
    if(v != ''){
        v=v.replace(/\D/g,"");
        v=v.replace(/(\d{2})(\d)/,"($1) $2");
        v=v.replace(/(\d{5})(\d)/,"$1-$2");
    }
    return v; 
}
