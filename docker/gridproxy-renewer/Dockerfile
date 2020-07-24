FROM cern/cc7-base

RUN curl -s -o /etc/yum.repos.d/egi.repo http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo \
  && curl -s -o /etc/pki/rpm-gpg/RPM-GPG-KEY-wlcg http://linuxsoft.cern.ch/wlcg/RPM-GPG-KEY-wlcg \
  && curl -s -o /etc/yum.repos.d/wlcg-centos7.repo http://linuxsoft.cern.ch/wlcg/wlcg-centos7.repo \
  && yum -y install ca-policy-egi-core ca-certificates voms-clients-cpp wlcg-voms-cms \
  && yum clean all && rm -rf /var/cache/yum

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl \
      && chmod +x ./kubectl \
      && mv ./kubectl /usr/local/bin/kubectl

COPY init-proxy /usr/local/bin/

CMD init-proxy
