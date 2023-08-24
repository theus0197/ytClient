// document.getElementsByClassName("confirm-form")[0].addEventListener("click", confirmForms);
document.getElementsByClassName("modal-close-alerts")[0].addEventListener("click", function(){
    document.getElementsByClassName('modal-alerts')[0].style.display = 'none'
});

document.getElementsByClassName("modal-close-alerts")[1].addEventListener("click", function(){
    document.getElementsByClassName('modal-alert-timer')[0].style.display = 'none'
});

(() => {

    var globalTimer = 0;
    var timerStarted = false;
    var liked = false;


    function insertElement(target, content, event){
        let element = document.querySelector(target)

        if(event == "insert") {
            element.innerHTML += content;
        }

        else if(event == "reinsert"){
            element.innerHTML = content
        }

        else if(event == "clear"){

        }

        else if(event == "value"){
            document.querySelector(target).value = content
        }

        else if(event == "src"){
            document.querySelector(target).src = content
        }
    }

    window.onload = () => {
        let queryString = window.location.search;
        getMainVideo(queryString)
        loadMoreVideos()
    }

    function get_random(arr){
        return arr[Math.floor((Math.random()*arr.length))];
    }

    async function getMainVideo(query){
        let r = new RequestHandler();
        r.baseUrl = '';
        const urlParams = new URLSearchParams(query);
        const videoId = urlParams.get('video_id');
        var video;
        if(videoId === null){
            let videos = await r.sendRequest(`videos/all`, 'GET')
            video = get_random(videos)
            location.href = '?video_id=' + video.pk
        }else{
            video = await r.sendRequest(`videos/id/${videoId}`, 'GET')
            if(video.length < 1){
                location.href = '/'
            }
            video = video[0]
        }
        insertElement('#ytPlayer', `https://www.youtube.com/embed/${video.fields.videocode}?enablejsapi=1&mute=0`, 'src')
        insertElement('.title-main span', `<h1>${video.fields.title}<p id="timer">Timer: 01:30</p></h1>`, 'reinsert')
        insertElement('.views', `${video.fields.views} mil views`, 'reinsert')
        insertElement('.likes', `${video.fields.likes} mil`, 'reinsert')

    }

    async function loadMoreVideos(){
        let r = new RequestHandler();
        r.baseUrl = '';

        let videos = await r.sendRequest(`videos/all`, 'GET')

        videos.forEach(element => {
            let queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const videoId = urlParams.get('video_id');

            if (videoId == element.pk){
                return;
            }

            let content = `
                <div class="next-video" onclick="window.location.href = '?video_id=${element.pk}'">
                    <div class="video" style="background-image: url(${element.fields.thumbnail});"></div>
                    <div class="title">
                        <span class="tt">${element.fields.title}</span>
                        <div class="details">
                            <span class="views">${element.fields.views} mil views</span>
                            <span class="likes">${element.fields.likes} mil curtidas</span>
                        </div>
                    </div>
                </div>
            `

            insertElement('.more-videos-container', content, 'insert')
        });
    }

    function triggerTimer(duration,display) {
        var timer = duration, minutes, seconds;
        timerStarted = true
        var interval = setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = 'Timer: ' + minutes + ":" + seconds;
            document.getElementById('timer-second').textContent = 'Tempo: ' + minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                display.textContent = "Timer: 00:00";
                globalTimer = timer
            }

            globalTimer = timer

        }, 1000);
    }


    function playvideo(){
        let player = document.getElementById('ytPlayer').contentWindow
        player.postMessage('{"event":"command","func":"playVideo","args":""}', '*')
        triggerTimer(90, document.getElementById('timer'));
    }

    async function likeVideo(){
        if(liked == true){
            alert('você não pode mais curtir este video!')
            return
        }

        else if(timerStarted == false){
            alert('O video precisar começar para você poder curtir')
        }else{
            if(globalTimer > 0){
                alert('Você precisa esperar o timer chegar a zero para curtir o video')
            }else{
                let queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const videoId = urlParams.get('video_id');

                const r = new RequestHandler;
                r.baseUrl = ''


                const response = await r.sendRequest(`videos/like/${videoId}`, 'POST')

                if(response.STATUS == 'FAIL'){
                    if(response.MESSAGE == 'RATELIMIT'){alert('Você atingiu o limite de curtidas diarias'); return;}
                }

                else if(response.STATUS == 'OK'){
                    if(response.MESSAGE == 'LIKED'){
                        console.log(response.AMOUNT);
                        document.getElementsByClassName('my-amount')[0].innerText = response.AMOUNT;
                    }
                }

                document.querySelector('.click-to-like-trigger').style.color = '#108df9';
                liked = true
            }
        }
    }


    document.getElementsByClassName('click-to-play-div')[0].addEventListener('click', function(){
        alert('video iniciado com sucesso!')
        playvideo()
        document.querySelector('.click-to-play-div').style.display = 'none';
        document.querySelector('.no-click').style.backgroundColor = 'transparent';
    });
    document.getElementsByClassName('container-like-main')[0].addEventListener('click', likeVideo);


})();