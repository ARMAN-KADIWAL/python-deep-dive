# Lab 79: Advanced Asyncio -- Building an Async Web Scraper

Fetch pages with asyncio/aiohttp and a synchronous requests baseline, parse identical HTML fields, retry transient failures and report per-URL outcomes.

## Concept in Hinglish

Async aur sync versions same URLs aur same parser use karte hain. 404 ko baar-baar retry nahi karte; 429 aur server errors par bounded backoff hai. Offline mode bhi actual HTTP sockets use karta hai, bas server local controlled fixture hota hai. Incomplete results par speedup claim nahi hota.

## Run

From the repository root, enter this folder. Python 3.8+ is required; the recorded validation uses Python 3.12.14. A virtual environment is recommended for third-party packages.

```bash
cd "Lab 79"
python3 -m pip install -r requirements.txt
python3 enhanced_scraper.py --offline
python3 main.py --offline
```

Offline mode uses actual HTTP requests against a controlled local server and needs no public API. To test the public example, omit `--offline`; this requires access to https://httpbin.org. A public HTTP/network failure is reported as a failure.

## Completion and corrections

- Used one shared HTML parser for synchronous, asynchronous and enhanced scrapers.
- Limited concurrency, validated configuration and released responses before retry sleeps.
- Recorded success, HTTP error, timeout and parse-error outcomes with attempt counts.
- Retried transient failures while avoiding unnecessary 404 retries.
- Only compared timings after both methods fetched the full identical URL list; the ratio is an observation, not a guaranteed speedup.

## Validation

```bash
python3 -m unittest discover -v -p "test_lab79.py"
```

The committed [verification/](verification/) directory contains the recorded local run. From the repository root, `python3 tools/validate_labs75_82.py --smoke` reruns all eight labs and writes fresh logs to `validation-output/`. Timing values and intentional race outcomes can change between runs. Persistent servers and interactive clients are covered by owned-server integration tests rather than left running by the smoke runner.

## Files

| File | Role |
|---|---|
| [async_scraper.py](async_scraper.py) | Runnable example or imported lab component |
| [enhanced_scraper.py](enhanced_scraper.py) | Runnable example or imported lab component |
| [http_fixture.py](http_fixture.py) | Controlled real HTTP test server |
| [main.py](main.py) | Runnable example or imported lab component |
| [page_parser.py](page_parser.py) | Runnable example or imported lab component |
| [sync_scraper.py](sync_scraper.py) | Runnable example or imported lab component |

The [complete guide](LAB_GUIDE.md) contains every final source file with its context. Missing endings and incremental class fragments were independently completed from the supplied lab requirements; these files are the runnable final implementation.
