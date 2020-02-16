# based on https://github.com/dask/dask-docker/blob/master/base/Dockerfile
# but more permissive about image size due to read-only requirement in openshift
# FROM daskdev/dask:2.9.0
FROM continuumio/miniconda3:4.7.12

RUN apt-get install gnupg2 -y \
    && wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | apt-key add - \
    && echo "deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ca-policy-egi-core \
    && apt-get purge -y gnupg2 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN conda install --yes \
    -c conda-forge \
    lz4 \
    xrootd==4.11.0 \
    tini==0.18.0 \
    && conda clean -tipsy

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    bokeh==1.3.4 \
    dask==2.10.1 \
    numpy==1.18.1 \
    pandas==0.25.3 \
    numba==0.48.0 \
    matplotlib==3.1.2 \
    scipy==1.4.1 \
    && conda clean -tipsy

RUN /opt/conda/bin/pip install --no-cache-dir coffea==0.6.33

RUN mkdir /opt/app

WORKDIR /opt/app

ENTRYPOINT ["tini", "-g", "--"]
