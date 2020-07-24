Coffea farm helm chart
----------------------

To install, first make a valid grid proxy and cd to this directory and run:
```
./preinstall.sh
helm install -f myvalues.yaml release .
```

Note: if you have a non-standard grid certificate location, please modify `preinstall.sh` accordingly.
