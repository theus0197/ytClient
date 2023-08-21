function wait(time) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, time);
    });
}

async function load(){
    var loadTime = document.getElementsByClassName('load-page')[0];
    //display none
    loadTime.style.display = 'none';
    var image = loadTime.getElementsByTagName('svg')[0];
    var paths = image.getElementsByTagName('path');
    var limit = paths.length;
    var i = 1;
    while(true){
        var dot = document.getElementById('dot-' + i);
        dot.style.fill = '#E91438';
        await wait(2000);
        dot.style.fill = '#fff';
        if(i >= limit){
            i = 1;
        }else{
            i++;
        }
    }
}

async function generateDouble(){
    var loadTime = document.getElementsByClassName('load-page')[0];
    //display flex
    loadTime.style.display = 'flex';
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/entry', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            loadTime.style.display = 'none';
            var element = document.getElementsByClassName('result-vela')[0];
            element.innerHTML = xhr.responseText;
            var dataId = document.getElementById('entry-value-color-confirmed').getAttribute('data-id');
            var percentWin = document.getElementsByClassName('percent-win')[0];
            var percentLoss = document.getElementsByClassName('percent-loss')[0];

            var colorWin = document.getElementsByClassName('entry-circly-value')[0].getAttribute('data-id');
            if(colorWin === 'red'){
                var color_1 = '#f12c4c';
                var color_2 = '#000';
            }else{
                var color_1 = '#000';
                var color_2 = '#f12c4c';
            }

            //convert dataId in number
            dataId = parseInt(dataId);
            percent_other = 100 - dataId;
            percentWin.getElementsByClassName('fill')[0].setAttribute("style","width:" + dataId + "%; background-color:" + color_1);
            percentWin.getElementsByClassName('fill')[0].innerHTML = dataId + '%';
            percentLoss.getElementsByClassName('fill')[0].setAttribute("style","width:" + percent_other + "%; background-color:" + color_2);
            percentLoss.getElementsByClassName('fill')[0].innerHTML = percent_other + '%';

            var applicationPercent = document.getElementsByClassName('application-percent')[0];
            applicationPercent.style.display = 'flex';
        } else {
            console.log('Request failed.  Returned status of ' + xhr.status);
        }
    }
    await wait(5000);
    xhr.send();
}

document.getElementsByClassName('btn-generate-vela')[0].addEventListener('click', generateDouble);
document.getElementsByClassName('reload-vela')[0].addEventListener('click', generateDouble);
load();