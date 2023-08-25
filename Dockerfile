# 
FROM python:3.11-slim

# Applications should run on port 8080 so NGINX can auto discover them.
EXPOSE 8080

# Make a new group and user so we don't run as root.
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

WORKDIR /app

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /app
RUN chown -R appuser:appgroup /app

USER appuser

# 
CMD ["uvicorn", "fasterid.fasterid:app", "--host", "0.0.0.0", "--port", "8080"]
