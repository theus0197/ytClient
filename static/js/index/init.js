function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


document.getElementsByClassName('rounded-container-start')[0].addEventListener('click', function(){
    document.getElementsByClassName('not-action')[0].style.display = 'none';
    document.querySelector("#video-apresentation").play()
})


async function autoStartVideo(){
    await sleep(6000);
    document.getElementsByClassName('not-action')[0].style.display = 'none';
    document.querySelector("#video-apresentation").play()
}

async function countdown(){
    var now_1 = new Date().getTime()
    minutes_add = ((60*60*290))
    var countDownDate =  now_1 + minutes_add;
    var x = setInterval(function() { 
        // Get today's date and time
        var now = new Date().getTime();
        
        // Find the distance between now and the count down date
        var distance = countDownDate - now;
        
        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Display the result in the element with id="demo"
        if(minutes === 0){
            document.getElementsByClassName("minute")[0].innerHTML = '00'
        }else{
            if(minutes < 10){
                minutes = '0' + String(minutes)
            }
            document.getElementsByClassName("minute")[0].innerHTML = minutes;
        }

        if(minutes === 16 && seconds < 46){
            document.getElementsByClassName('vaible-len')[0].innerHTML = '3'
        }else if(minutes === 17 && seconds < 10){
            document.getElementsByClassName('vaible-len')[0].innerHTML = '7'
        }

        if(seconds === 0){
            document.getElementsByClassName("seconds")[0].innerHTML = '00';
        }else{
            if(seconds < 10){
                seconds = '0' + String(seconds)
            }
            document.getElementsByClassName("seconds")[0].innerHTML = seconds;
        }
        
        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            //document.getElementById("demo").innerHTML = "EXPIRED";
        }
    }, 1000);
}

autoStartVideo();
countdown();
