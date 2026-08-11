# Build context is the grpc-hello-world/ folder (see docker-compose.yml)
# so this Dockerfile can reach both proto/ and client/.
FROM python:3.11-slim

WORKDIR /app

COPY client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generate the client-side pb2 stubs from the shared .proto into their own
# folder, kept separate from the server's generated stubs.
COPY proto/ ./proto/
RUN mkdir -p generated && \
    python -m grpc_tools.protoc \
        -I proto \
        --python_out=generated \
        --grpc_python_out=generated \
        proto/helloworld.proto

COPY client/client.py ./client.py

ENV PYTHONPATH=/app/generated

CMD ["python", "client.py"]
