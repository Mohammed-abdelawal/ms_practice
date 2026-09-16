"""Same function as functions/node/hello.js -- one service can mix runtimes."""

import json
import sys


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    name = params.get("name", "world")

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "message": f"Hello, {name}!",
            "runtime": f"python {sys.version.split()[0]}",
        }),
    }
