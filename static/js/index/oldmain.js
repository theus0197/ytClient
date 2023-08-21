function init_timer(timer){
    let time = 30;
    const interval = setInterval(() => {
        --time
        timer.innerHTML = time + "s";
        if(time == 0){
            clearInterval(interval);
            timer.innerHTML = '30s'
        }
    }, 1000);
}

document.querySelector("#play").addEventListener("click", (event) => {
    active = true;
    document.getElementById("ytPlayer").contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}','*');
    init_timer(timer);
   
    setTimeout(() => {
        fetch("/confirm/play", {
            "method": "POST",
            "headers": {'Accept': 'application/json','Content-Type': 'application/json'}
         }).then((response) => response.json()).then((data) => {
            frame = '<iframe id="ytPlayer"  frameborder="0"  allowfullscreen="1" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" title="YouTube video player" width="95%" height="90%" src="' + data['containers']['link'] + '?enablejsapi=1&mute=1"></iframe>'
            amount = data['containers']['amount']
            document.getElementsByClassName('main-video-container')[0].innerHTML = frame
            document.getElementsByClassName('my-amount')[0].innerText = amount
        })
        active = false;
    }, 30000);
    
});