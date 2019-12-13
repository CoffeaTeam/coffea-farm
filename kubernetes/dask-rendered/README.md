Pre-rendered helm chart for dask

The `manifest.yaml` was initially constructed with the recipe:
```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
helm repo add dask https://helm.dask.org/
helm repo update
helm template coffea-dask dask/dask > manifest.yaml
```

After configuration of `values.yaml`, a new manifest can be rendered using
```
helm template --values values.yaml coffea-dask dask/dask > manifest.yaml
```
