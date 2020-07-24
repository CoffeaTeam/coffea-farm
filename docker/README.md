Build and test dask image
```
docker build -t coffeateam/coffea-dask:0.1.x coffea-dask
docker run -it --rm coffeateam/coffea-dask:0.1.x /bin/bash
```

Build and test proxy image
```
docker build -t coffeateam/gridproxy-renewer:0.1.x gridproxy-renewer
docker run -v ~/.globus/:/globus -e VO=cms -e CERT=/globus/usercert.pem -e KEY=/globus/userkey.pem coffeateam/gridproxy-renewer:0.1.x
```
