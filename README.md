# fasterid
Identifier generator based on FastAPI and [`erdi8`](https://github.com/athalhammer/erdi8-py)

## Disclaimer

This software intentionally has no license attached. It does not need to comply to the GPL-3.0 license of `erdi8` as the `erdi8` copyright holder and the author of `fasterid` are the same person. __Please get in touch if you plan to use this in a commercial setting.__

## Quick start
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ cp template.env .env


$ uvicorn fasterid:app
	INFO:     Started server process [116821]
	INFO:     Waiting for application startup.
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

$ curl http://127.0.0.1:8000 -X POST
{"@id":"https://example.org/k7zydqrp64","timestamp":"1970-01-01T00:00:00.000001"}

# Call http://127.0.0.1:8000/docs for API info in a browser
```

**Test**
```
# From a different terminal
$ while true; do printf "$(curl -X POST http://127.0.0.1:8000)\n" >> ids; done

# After some seconds stop with: CTRL+C
$ head ids
{"@id":"https://example.org/ptzxm3mz85","timestamp":"1970-01-01T00:00:00.301453"}
{"@id":"https://example.org/tfzwsfhbb6","timestamp":"1970-01-01T00:00:00.317324"}
{"@id":"https://example.org/y2zvyscnd7","timestamp":"1970-01-01T00:00:00.333308"}
{"@id":"https://example.org/cnzv657yg8","timestamp":"1970-01-01T00:00:00.348514"}
{"@id":"https://example.org/h8ztch49j9","timestamp":"1970-01-01T00:00:00.365080"}
{"@id":"https://example.org/mvzsjtymmb","timestamp":"1970-01-01T00:00:00.381241"}
{"@id":"https://example.org/rgzrr6txpc","timestamp":"1970-01-01T00:00:00.395853"}
{"@id":"https://example.org/w3zqxjq8rd","timestamp":"1970-01-01T00:00:00.410346"}
{"@id":"https://example.org/zpzq4wkktf","timestamp":"1970-01-01T00:00:00.428683"}
{"@id":"https://example.org/f9zpb8fwwg","timestamp":"1970-01-01T00:00:00.455372"}

```

## Advanced

The service accepts also two optional parameters: `prefix` and `number`. The first can be used for creating individual identifiers with a prefix, the second is creating a batch with a certain number of ids. If `application/ld+json` is provided in the accept header the `prefix` or the `FASTERID_ID_DEFAULT_PREFIX` environment setting to create valid RDF. In that case, the generated erdi8 identifier MUST form a valid absolute IRI together with the provided `prefix` or `FASTERID_ID_DEFAULT_PREFIX`. The `number` and `prefix` parameters can be configured respecting max batch size and prefix length.

```
$ curl -sX POST http://127.0.0.1:8000   --data '{"number": 5, "prefix": "https://example.com/"}'   -H "content-type: application/json" -H "accept: application/ld+json" | jq
[
  {
    "@id": "https://example.com/fyyjrzbjqv",
    "https://schema.org/dateCreated": "1970-01-01T00:00:00.056241",
    "https://schema.org/identifier": "fyyjrzbjqv"
  },
  {
    "@id": "https://example.com/kkyhyc6vsw",
    "https://schema.org/dateCreated": "1970-01-01T00:00:00.056315",
    "https://schema.org/identifier": "kkyhyc6vsw"
  },
  {
    "@id": "https://example.com/q6yh5q36vx",
    "https://schema.org/dateCreated": "1970-01-01T00:00:00.056370",
    "https://schema.org/identifier": "q6yh5q36vx"
  },
  {
    "@id": "https://example.com/tsygc2xhxy",
    "https://schema.org/dateCreated": "1970-01-01T00:00:00.056423",
    "https://schema.org/identifier": "tsygc2xhxy"
  },
  {
    "@id": "https://example.com/ydyfjdstzz",
    "https://schema.org/dateCreated": "1970-01-01T00:00:00.056467",
    "https://schema.org/identifier": "ydyfjdstzz"
  }
]
```

## Docker

```
docker build -t fasterid .
docker run -d -p 80:80 fasterid
# OR
docker run -d -p 80:80 -e FASTERID_DEFAULT_PREFIX="" fasterid
# OR
docker run -d -p 80:80 -e FASTERID_DEFAULT_PREFIX="https://w3id.org/myspace/" -e FASTERID_ALWAYS_RDF="True" fasterid
# OR
docker run --log-driver=awslogs -d -p 80:80 -e FASTERID_DEFAULT_PREFIX="" fasterid
# OR
docker run --log-driver=awslogs -d -v /home/ec2-user/latest-id.txt:/fasterid-0.1.2/last-id.txt  -e FASTERID_DEFAULT_PREFIX="" -p 80:80 fasterid
````

## Docker Compose

```
# with postgres by default
docker compose up
```