FROM ubuntu:jammy

EXPOSE 80
RUN apt update && apt install wget python3 python3-venv -y

ARG FASTER_ID_VERSION="0.1.2"
RUN wget https://github.com/athalhammer/fasterid/archive/refs/tags/v${FASTER_ID_VERSION}.tar.gz
RUN tar -xzf v${FASTER_ID_VERSION}.tar.gz

RUN python3 -m venv /opt/env
ENV PATH="/opt/env/bin:$PATH"
WORKDIR fasterid-${FASTER_ID_VERSION}
RUN pip install -r requirements.txt

CMD ["uvicorn", "fasterid:app", "--host", "0.0.0.0", "--port", "80"]
