# Lab 80: Socket Programming Basics - Introduction to Sockets

Create TCP and UDP sockets, run matching clients and servers, handle complete TCP messages, close connections cleanly and verify full echo responses while measuring latency.

## Concept in Hinglish

Socket communication ka endpoint hai. TCP byte stream hai: ek send ka matlab ek recv mein poora message milna nahi. network_core.py four-byte length header aur complete reads use karta hai. UDP mein har datagram ki boundary hoti hai, lekin delivery/order guarantee nahi. Matching client aur server versions saath use karo.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 80"
python3 basic_socket.py
python3 socket_comparison.py
```

These examples use the Python standard library.

## TCP echo and performance test

Keep this running in terminal 1:

```bash
python3 tcp_server.py
```

In terminal 2, in the same folder on the same machine:

```bash
python3 tcp_client.py
python3 socket_context_manager.py
python3 socket_performance_test.py --messages 100 --size 1024
```

Exit the interactive client with `quit`. The context-manager example and benchmark use the echo server on port 8888.

## Robust command server

Terminal 1: `python3 robust_server.py`

Terminal 2: `python3 robust_client.py`

Commands: `help`, `time`, `echo Hello World`, `quit`, `exit`, `bye`. This pair uses port 7777, independently of the echo benchmark.

## UDP

Terminal 1: `python3 udp_server.py`

Terminal 2: `python3 udp_client.py`

This pair uses UDP port 9999. Type `quit` to end the client.

## TCP protocol and port selection

TCP messages use a four-byte unsigned big-endian byte length followed by UTF-8 content, with a 1 MiB frame limit. Use the matching clients in this folder; plain raw-text clients from earlier handout stages do not speak this framing. Both terminals must target the same host and port. Servers default to localhost.

If another lab already uses the port, select another port on both processes, for example `python3 tcp_server.py --port 8890` and the corresponding client with `--port 8890`. Ctrl+C stops the server and closes its owned client sockets.

## Completion and corrections

- Completed the truncated performance statistics and script entry point.
- Added length-prefixed UTF-8 framing, sendall and complete reads for TCP.
- Aligned every supplied TCP client, context-manager example and benchmark with the same framing.
- Validated full echo contents before recording each latency sample; samples reset between runs.
- Added bounded UDP reads/timeouts and clean shutdown. TIME_WAIT is a normal TCP state, not proof that close failed.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab80.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [basic_socket.py](basic_socket.py) | Runnable example or imported lab component |
| [client_core.py](client_core.py) | Shared client connection lifecycle |
| [network_core.py](network_core.py) | Shared framing and server lifecycle |
| [robust_client.py](robust_client.py) | Runnable example or imported lab component |
| [robust_server.py](robust_server.py) | Runnable example or imported lab component |
| [socket_comparison.py](socket_comparison.py) | Runnable example or imported lab component |
| [socket_context_manager.py](socket_context_manager.py) | Runnable example or imported lab component |
| [socket_performance_test.py](socket_performance_test.py) | Runnable example or imported lab component |
| [tcp_client.py](tcp_client.py) | Runnable example or imported lab component |
| [tcp_server.py](tcp_server.py) | Runnable example or imported lab component |
| [udp_client.py](udp_client.py) | Runnable example or imported lab component |
| [udp_server.py](udp_server.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
