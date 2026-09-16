// A Lambda handler: no server, no routes, no app.listen. The platform -- or
// serverless-offline, locally -- receives the HTTP request, turns it into an
// `event`, calls this function, and turns the return value into the response.
exports.handler = async (event) => {
    const name = event.queryStringParameters?.name ?? "world";

    return {
        statusCode: 200,
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
            message: `Hello, ${name}!`,
            runtime: `node ${process.version}`
        })
    };
};
