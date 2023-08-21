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
            options.body = JSON.stringify(data);
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
