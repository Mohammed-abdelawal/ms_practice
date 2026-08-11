import os
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

# In docker-compose this is the server's service name; locally it falls back
# to localhost so the script still works outside a container.
SERVER_ADDR = os.environ.get("GRPC_SERVER_ADDR", "localhost:50051")


def run():
    # A channel is the connection to the server; the stub is the
    # generated "fake local object" whose methods actually go over the wire.
    with grpc.insecure_channel(SERVER_ADDR) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = call_with_retry(stub)
    print("Greeter client received: " + response.message)


def call_with_retry(stub, retries=10, delay=1):
    """The server container may still be starting up when we connect, so
    retry a few times instead of failing immediately."""
    for attempt in range(1, retries + 1):
        try:
            return stub.SayHello(helloworld_pb2.HelloRequest(name="World"))
        except grpc.RpcError:
            if attempt == retries:
                raise
            print(f"Server not ready yet (attempt {attempt}/{retries}), retrying...")
            time.sleep(delay)


if __name__ == "__main__":
    run()
