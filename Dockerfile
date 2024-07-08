FROM python:3.12.3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
postgresql-client \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -rf /tmp

COPY . .

ENV PORT 5000

EXPOSE $PORT

ENV FLASK_APP=hbnb.py
ENV FLASK_ENV=development
ENV DATABASE_URL=sqlite:///db.db
ENV JWT_SECRET_KEY=secret_passkey

CMD gunicorn hbnb:app -w 2 -b 0.0.0.0:$PORT
