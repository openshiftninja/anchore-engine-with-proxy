FROM anchore/anchore-engine

# i seem to have an issue with the epel repo, and I don't really need it so disable it for this install
RUN yum-config-manager --disable epel
RUN yum -y update && yum -y install patch && yum -y install libffi-devel

COPY . /root/anchore-engine-with-proxy
# apply simple patch to proxy the requests to https://ancho.re
RUN cd /root/anchore-engine-with-proxy && patch -d/ -p0 < feeds.py.patch
# add the proxy script into the feed service, where it is actually used
COPY ./requests_proxy.py /root/anchore-engine/anchore_engine/clients/feeds/feed_service/
# do the normal install which will update the feeds.py
RUN cd /root/anchore-engine/ && pip install --upgrade .

# normal anchore-engine entry point
CMD /usr/bin/anchore-engine
