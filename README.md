# skogaming


# Create Docker network

```
docker create network my-net
```


# Redis

```
docker run --name redis-instance -itd -p 6379:6379 --network my-net -u 1007 -v /tmp:/data redis
```


# Leaderboard (Flask + uwsgi with 4 processes each with 2 threads )

```
docker run -itd --name leaderboard --network my-net -p 6001:6001 harnit/uwsgi-leaderboard:v3
```


# Otel Collector

```
docker run -d --rm -e SPLUNK_ACCESS_TOKEN=<insert-token> -e SPLUNK_MEMORY_TOTAL_MIB=1024 \
    -e SPLUNK_REALM=us0 -p 14268:14268 -p 9411:9411 -p 9943:9943 -v otel-config.yaml:/etc/collector.yaml:ro \
    --name otelcol --network my-net quay.io/signalfx/splunk-otel-collector:latest
```


# Leaderboard fetcher (and async reporter)

```
docker run -itd --name asyncfetcher -pull=always --network my-net harnit/asyncleaderfetcher:v1
```



# Log onto sko-gaming-instance (gcloud)


# nginx conf files ->

```
sudo vim /etc/nginx/nginx.conf
```
 
and  

```
sudo vim /etc/nginx/sites-available/default
```

# Location of web pages ->

```
/var/www/gaming
```


# Restarting nginx

```
sudo systemctl restart nginx
```


Certbot is installed on the server (SSL setup)




# Data flow

```
External Client (JS client via Web Browser) -> Nginx -> Flask server -> Redis
                                                                     -> Otel collector -> Splunk Infra Mon
```

```
Async Fetcher -> Flask server -> Redis

              -> Otel-collector -> Splunk Infra Mon 
```
