FROM centos:7
ENV container docker

MAINTAINER Prashanth_M

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
    systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*; \
    rm -f /etc/systemd/system/*.wants/*; \
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*; \
    rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN \
    yum -y update && \
    yum -y install initscripts && \
    yum -y install curl git vim vim-enhanced wget htop man python unzip tar openssh-server* open-ssh-client* && \
    yum -y install tcpdump && \
    yum clean expire-cache && \
    yum -y clean all

RUN service sshd restart

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
