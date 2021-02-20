FROM python:3.6-alpine

COPY requirements.txt ./

RUN apk --update --no-cache add curl gcc libc-dev linux-headers

RUN pip install --no-cache-dir -r requirements.txt

COPY leaderboard-server.py ./

#CMD python leaderboard-server.py

CMD /usr/local/bin/uwsgi --http :6001 --wsgi-file leaderboard-server.py --callable app --master --enable-threads --processes 4 --threads 2

HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://localhost:6000/healthz || exit 1
