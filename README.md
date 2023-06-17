# fasterid
Identifier generator based on FastAPI and [`erdi8`](https://github.com/athalhammer/erdi8-py)


## Quick start
```
$ pip install -r requirements.txt
$ cat fasterid.env
    ERDI8_STRIDE = "453459956896834"
    ERDI8_START = "b222222222"
    ERDI8_SAFE = "True"
    FASTERID_FILENAME = "last-id.txt"
    FASTERID_MAX_NUM = 50
    FASTERID_MAX_PREFIX_LEN = 100

$ uvicorn fasterid:app
	INFO:     Started server process [116821]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

$ curl http://127.0.0.1:8000 -X POST
{"id":["k7zydqrp64"]}

# Call http://127.0.0.1:8000/docs for API info in a browser
```

**Test**
```
# From a different terminal
$ while true; do printf "$(curl -X POST http://127.0.0.1:8000)\n" >> ids; done

# After some seconds stop with: CTRL+C
$ head ids
    {"id":["ptzxm3mz85"]}
    {"id":["tfzwsfhbb6"]}
    {"id":["y2zvyscnd7"]}
    {"id":["cnzv657yg8"]}
    {"id":["h8ztch49j9"]}
    {"id":["mvzsjtymmb"]}
    {"id":["rgzrr6txpc"]}
    {"id":["w3zqxjq8rd"]}
    {"id":["zpzq4wkktf"]}
    {"id":["f9zpb8fwwg"]}

## Advanced

The service accepts also two parameters: `prefix` and `number`. The former is for creating individual identifiers, the second is creating a batch with a certain number of ids. Both parameters are optional and can be configured respecting max batch size and prefix length.

```
$ curl -X POST localhost:8000 --data '{"number": 5, "prefix": "https://example.com/"}' -H "content-type: application/json" | jq
    {
     "id": [
        "https://example.com/nvyywq9pnb",
        "https://example.com/sgyy435zqc",
        "https://example.com/x3yx9f2bsd",
        "https://example.com/bpywgrwnvf",
        "https://example.com/g9yvp4ryxg"
     ]
    }
```
