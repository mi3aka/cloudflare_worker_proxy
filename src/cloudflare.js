addEventListener('fetch', event => {
    const { request } = event;
    const { headers } = request;
    const contentType = headers.get('content-type') || '';

    if (request.method === 'POST') {
        if (contentType.includes('application/json')) {
            return event.respondWith(handleRequest(request));
        } else {
            return event.respondWith(fetch("https://welcome.developers.workers.dev"));
        }
    } else {
        return event.respondWith(fetch("https://welcome.developers.workers.dev"));
    }
});


async function handleRequest(request) {
    const req = await request.json();
    const url = req["url"];
    const method = req["method"];
    const headers = JSON.parse(atob(req["headers"]));//example: base64encode('{"Content-Type":"application/x-www-form-urlencoded"}')
    if (method === 'GET') {
        const init = {
            method: 'GET',
            headers: headers
        };
        const response = await fetch(url, init);//https://httpbin.org/get
        // const results = await response.text();
        // return new Response(results, init);
        return response;
    } else if (method === 'POST') {
        const body = atob(req["body"]);
        const init = {
            method: 'POST',
            headers: headers,
            body: body
        };
        const response = await fetch(url, init);//https://httpbin.org/post
        // const results = await response.text();
        // return new Response(results, init);
        return response;
    }
}
