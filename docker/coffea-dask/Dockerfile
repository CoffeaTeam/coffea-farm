# based on https://github.com/dask/dask-docker/blob/master/base/Dockerfile
# but more permissive about image size due to read-only requirement in singularity
# FROM daskdev/dask:2.9.0
FROM continuumio/miniconda3:4.7.12

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    dask==2.9.0 \
    lz4 \
    numpy==1.17.4 \
    pandas==0.25.2 \
    tini==0.18.0 \
    xrootd \
    numba \
    && conda clean -tipsy

RUN /opt/conda/bin/pip install --no-cache-dir coffea

RUN mkdir /opt/app

WORKDIR /opt/app

ENTRYPOINT ["tini", "-g", "--"]
