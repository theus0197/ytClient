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


(async () => {
    let saveChanges = document.getElementById('save-changes');

    function convertColorToJson(string) {
        return `{"color": "${string}"}`
    }

    function sendToRoute() {
        let dataToSend = []

        saveChanges.addEventListener('click', async (e) => {
            let r = new RequestHandler();
            r.baseUrl = '';
            let colors = document.querySelectorAll('.opts input')
            let ratelimit = document.querySelector('#ratelimit').value
            
            colors.forEach(element => {
                if (element.name) {
                    data = {
                        "nameUpdate": `${element.name}`,
                        "type": "colorScheme",
                        "value": element.value   //convertColorToJson(element.value)
                    }
                    dataToSend.push(data)
                }
            });

            //await r.sendRequest('/panel/configs/updateRatelimit', 'PUT', ratelimit)

            /*dataToSend.forEach(async (element, index) => {
                await r.sendRequest(`/panel/configs/updateColors`, 'PUT', JSON.stringify(element))
            })*/
            var xhr = new XMLHttpRequest();
            xhr.open('PUT', '/panel/configs/updateColors', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function() {
                if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        if(response.status){
                            alert('Alterações salvas com sucesso!');
                        }else{
                            alert(response.message);
                        }
                }else{
                    alert('Erro ao realizar chamada!');
                }
            }
            xhr.send(JSON.stringify({
                'listData': dataToSend
            }));
            
        })

    }
    sendToRoute()
})();