```
⚠️ this repo is still under construction
```

# Hyko worker 

This is an alternative implementation for `compute machines` on hyko, using `arq` workers. 


## Run using docker

```bash
git clone git@github.com:BIGmama-technology/Hyko-worker.git
cd Hyko-worker/
```

```bash
docker build -t hyko_worker .
docker run --add-host="redis.traefik.me:127.17.0.1" hyko_worker:latest
```
