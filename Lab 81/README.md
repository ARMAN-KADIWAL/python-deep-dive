# Lab 81: Building a Simple Client-Server Application

Build single-client and threaded servers with command responses, then verify simultaneous clients against the same application protocol.

## Concept in Hinglish

Single server ek client ko handle karke next leta hai. Threaded server har client ke liye worker thread start karta hai. Registry lock active-client count ko protect karta hai. Welcome aur command responses framed hain, isliye ek doosre mein merge nahi hote.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 81"
python3 server_threaded.py
```

These examples use the Python standard library.

## Two terminals

Terminal 1: choose `python3 server.py` for the single-client server, or `python3 server_threaded.py` for concurrent clients. Both default to port 12345; run one per port.

Terminal 2:

```bash
python3 client.py
python3 test_multiple_clients.py --clients 5
```

Commands: `hello`, `time`, `clients`, `help`, `exit`. Exit the interactive client before launching the automated test. Run the multi-client test against server_threaded.py.

## TCP protocol and port selection

TCP messages use a four-byte unsigned big-endian byte length followed by UTF-8 content, with a 1 MiB frame limit. Use the matching clients in this folder; plain raw-text clients from earlier handout stages do not speak this framing. Both terminals must target the same host and port. Servers default to localhost.

If another lab already uses the port, select another port on both processes, for example `python3 server_threaded.py --port 8890` and the corresponding client with `--port 8890`. Ctrl+C stops the server and closes its owned client sockets.

## Completion and corrections

- Integrated the incremental source fragments into complete runnable server.py and client.py files.
- Retained a single-client server and a separate threaded server for comparison.
- Protected the client registry, framed welcome/response messages and closed clients during shutdown.
- Automated client failures propagate to a nonzero process exit status.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab81.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [client.py](client.py) | Runnable example or imported lab component |
| [client_core.py](client_core.py) | Shared client connection lifecycle |
| [network_core.py](network_core.py) | Shared framing and server lifecycle |
| [server.py](server.py) | Runnable example or imported lab component |
| [server_threaded.py](server_threaded.py) | Runnable example or imported lab component |
| [test_multiple_clients.py](test_multiple_clients.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
