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
    FASTERID_ID_PROPERTY = "https://schema.org/identifier"

$ uvicorn fasterid:app
	INFO:     Started server process [116821]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

$ curl http://127.0.0.1:8000 -X POST
{"@id": "k7zydqrp64"}

# Call http://127.0.0.1:8000/docs for API info in a browser
```

**Test**
```
# From a different terminal
$ while true; do printf "$(curl -X POST http://127.0.0.1:8000)\n" >> ids; done

# After some seconds stop with: CTRL+C
$ head ids
{"@id":"ptzxm3mz85"}
{"@id":"tfzwsfhbb6"}
{"@id":"y2zvyscnd7"}
{"@id":"cnzv657yg8"}
{"@id":"h8ztch49j9"}
{"@id":"mvzsjtymmb"}
{"@id":"rgzrr6txpc"}
{"@id":"w3zqxjq8rd"}
{"@id":"zpzq4wkktf"}
{"@id":"f9zpb8fwwg"}
```

## Advanced

The service accepts also three parameters: `prefix`, `number`, and `rdf`. The first can be used for creating individual identifiers, the second is creating a batch with a certain number of ids, the third uses the `prefix` to create valid RDF. All parameters are optional but `rdf` depends on `prefix`: the concatenation of `prefix` and the generated erdi8 identifier MUST form a valid absolute IRI. `number` and `prefix` and can be configured respecting max batch size and prefix length.

```
$ curl -X POST http://127.0.0.1:8000 --data '{"number": 5, "prefix": "https://example.com/", "rdf": true}' -H "content-type: application/json" | jq
[
  {
    "@id": "https://example.com/t7t9vt26f4",
    "https://schema.org/identifier": "t7t9vt26f4"
  },
  {
    "@id": "https://example.com/xtt935whh5",
    "https://schema.org/identifier": "xtt935whh5"
  },
  {
    "@id": "https://example.com/cft88hrtk6",
    "https://schema.org/identifier": "cft88hrtk6"
  },
  {
    "@id": "https://example.com/h2t7fvn5n7",
    "https://schema.org/identifier": "h2t7fvn5n7"
  },
  {
    "@id": "https://example.com/mnt6n7hgq8",
    "https://schema.org/identifier": "mnt6n7hgq8"
  }
]
```
