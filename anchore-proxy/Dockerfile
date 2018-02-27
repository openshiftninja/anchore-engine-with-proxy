FROM centos

EXPOSE 5000

RUN yum -y update && yum -y install epel-release
# fix minor https issue with epel
RUN sed -i "s/mirrorlist=https/mirrorlist=http/" /etc/yum.repos.d/epel.repo
RUN yum clean all -y
RUN yum -y install python34-devel python34-pip openssl-devel && yum clean all -y
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade -r /app/requirements.txt

CMD python3 /app/anchore-proxy.py