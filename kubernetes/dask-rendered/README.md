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

A grid proxy is expected, provided as a secret. Create one with the usual `voms-proxy-init` incantation, followed by:
```
kubectl create secret generic grid-proxy --from-file=x509up=$(voms-proxy-info --path) --dry-run -o yaml --save-config | kubectl apply -f -
```
