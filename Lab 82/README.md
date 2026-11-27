# Lab 82: Multi-client Server with Threading

Combine per-client threads, locked shared history/counters, complete messages, automated clients, verified stress tests and graceful shutdown.

## Concept in Hinglish

Har client ka message count lock ke andar update hota hai. History last 100 messages tak bounded hai. Disconnect par active registry aur per-client counter clean hote hain. Server monitor har expected echo check karta hai; sirf response milne ko successful test nahi maanta.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 82"
python3 multi_server.py
```

These examples use the Python standard library.

## Server and clients

Terminal 1: `python3 multi_server.py`

Terminal 2:

```bash
python3 test_client.py
python3 test_client.py Client-A --automated --messages 7
python3 multi_client_test.py --clients 5
python3 server_monitor.py
```

Commands: `time`, `clients`, `info`, `history`, `stats`, `quit`, or any text to echo. Exit the interactive client with `quit` before the following commands.

## TCP protocol and port selection

TCP messages use a four-byte unsigned big-endian byte length followed by UTF-8 content, with a 1 MiB frame limit. Use the matching clients in this folder; plain raw-text clients from earlier handout stages do not speak this framing. Both terminals must target the same host and port. Servers default to localhost.

If another lab already uses the port, select another port on both processes, for example `python3 multi_server.py --port 8890` and the corresponding client with `--port 8890`. Ctrl+C stops the server and closes its owned client sockets.

## Completion and corrections

- Merged all handout class/method fragments into a complete multi_server.py implementation.
- Added locked bounded history, accurate client counters and disconnect cleanup.
- Handled partial/multiple TCP frames, malformed input, idle timeouts and graceful shutdown.
- Automated clients and the monitor verify response contents and report actual failed clients.
- Removed unsolicited application keepalive responses that could be confused with command replies.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab82.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [client_core.py](client_core.py) | Shared client connection lifecycle |
| [multi_client_test.py](multi_client_test.py) | Runnable example or imported lab component |
| [multi_server.py](multi_server.py) | Runnable example or imported lab component |
| [network_core.py](network_core.py) | Shared framing and server lifecycle |
| [server_monitor.py](server_monitor.py) | Runnable example or imported lab component |
| [test_client.py](test_client.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
