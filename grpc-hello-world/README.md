# gRPC Hello World - Containerized with Docker Compose

This is a containerized gRPC application split into separate server and client services that communicate via Docker Compose networking.

## Project Structure

```
grpc-hello-world/
├── proto/                 # Shared protobuf definitions
│   └── helloworld.proto   # gRPC service contract
├── server/                # Server service
│   ├── Dockerfile
│   ├── server.py
│   └── requirements.txt
├── client/                # Client service
│   ├── Dockerfile
│   ├── client.py
│   └── requirements.txt
├── Makefile               # Unified command interface
├── docker-compose.yml     # Orchestration config
└── README.md
```

## How It Works

1. **Proto Files** (`proto/`): Shared `.proto` definitions — both server and client Dockerfiles generate their own pb2 stubs from this single source.
2. **Generated Stubs** (`.gitignore`d): Each container generates `helloworld_pb2.py` and `helloworld_pb2_grpc.py` at build time into its own `generated/` folder.
3. **Docker Compose**: Defines two services on a shared network (`grpc-net`):
   - **server**: Listens on port 50051 (exposed to host)
   - **client**: Connects via `GRPC_SERVER_ADDR=server:50051` (service name on the network)

## Quick Start

### Build & Run (Most Common)
```bash
make up
```
This builds both images and runs them. You'll see the server start, then the client connect and receive a response.

### Run Detached
```bash
make up-d
```
Start services in the background.

### Check Status
```bash
make ps      # Show running containers
make logs    # Tail all logs
make logs-server  # Server logs only
make logs-client  # Client logs only
```

### Clean Up
```bash
make down    # Stop and remove containers
make clean   # Remove containers, networks, and images
```

## Makefile Commands

| Command | Purpose |
|---------|---------|
| `make build` | Build both images only (don't run) |
| `make up` | Build and run both services (blocking) |
| `make up-d` | Build and run in background |
| `make restart` | Restart containers |
| `make logs` | Tail logs from all services |
| `make logs-server` | Tail server logs only |
| `make logs-client` | Tail client logs only |
| `make ps` | List running containers |
| `make down` | Stop and remove containers |
| `make clean` | Remove all artifacts (containers, networks, images) |

## Environment Variables

- **`GRPC_SERVER_ADDR`** (client only): Server address in docker-compose. Set by docker-compose.yml to `server:50051`. Defaults to `localhost:50051` for local testing.

## Dockerfiles Explained

### Server Dockerfile
- Installs gRPC dependencies
- Copies `.proto` file and generates server stubs into `generated/`
- Copies `server.py` and runs it
- Exposes port 50051

### Client Dockerfile
- Installs gRPC dependencies
- Copies `.proto` file and generates client stubs into its own `generated/` folder
- Copies `client.py` and runs it
- Includes retry logic to wait for server to start

## Local Testing (Without Docker)

To test locally with your `.venv`:

1. **Generate pb2 files**:
   ```bash
   python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/helloworld.proto
   ```

2. **Run server** (in one terminal):
   ```bash
   python server/server.py
   ```

3. **Run client** (in another):
   ```bash
   python client/client.py
   ```

## What's Generated

During the Docker build, each container generates:
- `helloworld_pb2.py` — Python protocol buffer classes
- `helloworld_pb2_grpc.py` — gRPC stubs and service base classes

These are **not committed** to git (see `.gitignore`); they're regenerated every build from `proto/helloworld.proto`.

## Extending

To add new RPC methods:
1. Edit `proto/helloworld.proto`
2. Rebuild: `make build` or just run `make up` (it rebuilds automatically)
3. Update `server/server.py` and `client/client.py` to use the new methods

The Dockerfiles will automatically re-generate the pb2 stubs for both server and client.
