FROM python:3.6-alpine

COPY requirements.txt ./

RUN apk --update --no-cache add curl

RUN pip install --no-cache-dir -r requirements.txt

COPY asyncLeaderFetcher.py ./

CMD python asyncLeaderFetcher.py

