# Copyright (C) 2023  Andreas Thalhammer
# Please get in touch if you plan to use this in a commercial setting.
FROM python:3.12-alpine

# uncomment below for postgresql
RUN apk update && apk add --no-cache bash postgresql-dev

EXPOSE 80

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "fasterid:app", "--host", "0.0.0.0", "--port", "80"]
