#!/usr/bin/env bash

openssl rsa -in ~/.globus/userkey.pem | kubectl create secret generic grid-cert \
  --from-file=usercert.pem=$HOME/.globus/usercert.pem \
  --from-file=userkey.pem=/dev/stdin \
  --dry-run -o yaml --save-config | kubectl apply -f -

kubectl create secret generic grid-proxy \
  --from-file=x509up=$(voms-proxy-info --path) \
  --dry-run -o yaml --save-config | kubectl apply -f -

kubectl create secret generic dask-tls-certs \
  --from-file=ca.crt \
  --from-file=ca.key \
  --from-file=hostcert.pem \
  --dry-run -o yaml --save-config | kubectl apply -f -
