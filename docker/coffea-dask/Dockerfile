# based on https://github.com/dask/dask-docker/blob/master/base/Dockerfile
# but more permissive about image size due to read-only requirement in openshift
FROM continuumio/miniconda3:4.8.2

RUN apt-get install gnupg2 -y \
    && wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | apt-key add - \
    && echo "deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ca-policy-egi-core \
    && apt-get purge -y gnupg2 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN conda install --yes --freeze-installed -c conda-forge \
    bokeh==2.2.3 \
    dask==2.30.0 \
    distributed==2.30.0 \
    matplotlib==3.3.2 \
    jupyter-server-proxy \
    lz4==3.1.0 \
    numba==0.51.2 \
    numpy==1.19.2 \
    pandas==1.1.4 \
    python-blosc==1.9.2 \
    scipy==1.5.3 \
    tini==0.18.0 \
    xrootd==5.0.2 \
    && conda clean -afy

RUN /opt/conda/bin/pip install --no-cache-dir \
    xxhash==2.0.0 \
    coffea==0.6.45

RUN mkdir /opt/app

WORKDIR /opt/app

ENTRYPOINT ["tini", "-g", "--"]
