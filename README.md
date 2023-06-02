# fasterid
Identifier generator based on FastAPI and [`erdi8`](https://github.com/athalhammer/erdi8-py)


## Quick start
```
$ pip install -r requirements.txt
$ cat fasterid.env
	ERDI8_SEED = "453459956896834"
	ERDI8_START = "b222222222"
	ERDI8_SAFE = "True"
	ERDI8_FILENAME = "last-id.txt"

$ uvicorn fasterid:app
	INFO:     Started server process [116821]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

$ curl http:127.0.0.1:8000 -X POST
{"id":"fmzz7cwc43"}

# Call http://127.0.0.1:8000/docs for API info in a browser
```

**Test**
```
# From a different terminal
$ while true; do printf "$(curl -X POST http://127.0.0.1:8000)\n" >> ids; done

# After some seconds stop with: CTRL+C
$ head ids
{"id":"fmzz7cwc43"}
{"id":"k7zydqrp64"}
{"id":"ptzxm3mz85"}
{"id":"tfzwsfhbb6"}
{"id":"y2zvyscnd7"}
{"id":"cnzv657yg8"}
{"id":"h8ztch49j9"}
{"id":"mvzsjtymmb"}
{"id":"rgzrr6txpc"}
...
```

