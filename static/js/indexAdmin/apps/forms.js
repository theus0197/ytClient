// document.getElementById('image-profile').addEventListener('click', function() {
//     document.getElementsByClassName('input-logo-image')[0].click();
// });

// document.getElementsByClassName('input-logo-image')[0].addEventListener('change', function() {
//     var input = this;
//     if(input.files && input.files[0]) {
//         var url = URL.createObjectURL(this.files[0]);
//         document.getElementById('image-profile').src = url;
//     }else{
//         url = document.getElementById('image-profile').src;
//     };
// });
// function validateInfo(){
//     value = document.getElementsByName('enterprise')[0].value;
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/panel/api/enterprise/validate/info', true);
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.onload = function() {
//         if (xhr.status === 200) {
//             var data = JSON.parse(xhr.responseText);
//             var statusInput = document.getElementsByClassName('status-enterprise')[0];
//             if(data.containers.validation){
//                 statusInput.classList.add('green');
//                 statusInput.classList.remove('red')
//             }else{
//                 document.getElementById('image-profile').src = data.containers.logo
//                 statusInput.classList.add('red');
//                 statusInput.classList.remove('green')
//                 }
//         } else {
//             alert('Erro ao realizar chamada!');
//         }
//     }
//     xhr.send(JSON.stringify({
//         'value': value
//     }));
// }

// function createEnterprise(){
//     if(document.getElementsByClassName('status-enterprise')[0].classList.contains('green')){
//         var inputImage = document.getElementsByClassName('input-logo-image')[0]
//         if(inputImage.value === '' || inputImage.value === null) {
//             var imgContent = ['url', document.getElementById('image-profile').src];
//             var name = document.getElementsByName('enterprise')[0].value;
//             var xhr = new XMLHttpRequest();
//                 xhr.open('POST', '/panel/api/enterprise/create', true);
//                 xhr.setRequestHeader('Content-Type', 'application/json');
//                 xhr.onload = function() {
//                     if (xhr.status === 200) {
//                         var data = JSON.parse(xhr.responseText);
//                         alert(data.message);
//                     } else {
//                         alert('Erro ao realizar chamada!');
//                     }
//                 }
//                 xhr.send(JSON.stringify({'name': name, 'image': imgContent}));
//         }else{
//             var reader = new FileReader();
//             reader.readAsDataURL(inputImage.files[0]);
//             reader.onload = function(e) {
//                 var data = e.target.result;
//                 var base64 = data.split(',')[1];
//                 var imgContent = ['base64', base64];
//                 var name = document.getElementsByName('enterprise')[0].value;
//                 var xhr = new XMLHttpRequest();
//                 xhr.open('POST', '/panel/api/enterprise/create', true);
//                 xhr.setRequestHeader('Content-Type', 'application/json');
//                 xhr.onload = function() {
//                     if (xhr.status === 200) {
//                         var data = JSON.parse(xhr.responseText);
//                         alert(data.message);
//                     } else {
//                         alert('Erro ao realizar chamada!');
//                     }
//                 }
//                 xhr.send(JSON.stringify({'name': name, 'image': imgContent}));
//             }
//         }
//     }
// }

// document.getElementsByClassName('btn-form-create')[0].addEventListener('click', createEnterprise)
// document.getElementsByName('enterprise')[0].addEventListener('keyup', validateInfo)

class RequestHandler {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async sendRequest(endpoint, method = 'GET', data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const options = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = data;
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}: ${response.statusText}`);
            }

            const responseData = await response.json();
            return responseData;
        } catch (error) {
            throw new Error(`Request failed: ${error.message}`);
        }
    }
}

(() => {
    function insertElement(target, content, event){
        let element = document.querySelector(target)

        if(event == "insert") {
            element.innerHTML = "";
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

    function randomGenerate() {
        return Math.floor(Math.random() * 100) + 1;
    }

    async function getInfoFromVideos(){
        document.getElementById('get-changes').addEventListener('click', async(e) => {
            let video = document.getElementById('url').value
            let likes = randomGenerate()
            let views = randomGenerate()

            const r = new RequestHandler();
            r.baseUrl = ''
            let data = await r.sendRequest(`/panel/configs/videos?id=${video}`, 'GET')

            insertElement('#input2', likes, 'value')
            insertElement('#input1', views, 'value')
            insertElement('#tt', data.response.title, 'value')
            insertElement('#url', data.code, 'value')
            insertElement('#thumb', data.response.thumbnail, 'src')
        })

        document.getElementById('save-get-changes').addEventListener('click', async(e) => {
            let code = document.getElementById('url').value
            let title = document.getElementById('tt').value
            let thumbnail = document.getElementById('thumb').src
            let likes = document.getElementById('input1').value
            let views = document.getElementById('input2').value
            let points = document.getElementById('pointsToEarn').value
            let doublePoints = document.getElementById('doublePoints').checked

            const r = new RequestHandler();
            r.baseUrl = ''

            await r.sendRequest(`/panel/configs/videos/create`, 'POST', JSON.stringify({code, title, thumbnail, likes, views, points, doublePoints}))
        })
    }
    getInfoFromVideos()
})();



