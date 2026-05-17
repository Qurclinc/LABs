# Its Debian uwu
FROM wordpress:5.8-php7.4-apache

RUN apt-get update -y && \ 
    apt-get install -y openssh-server bash sudo nano vim python3 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd adam -m -s /bin/bash

RUN echo 'adam:s3cr3tP@55w0rD!' | chpasswd

USER www-data

RUN mkdir -p /var/www/html/wp-content/uploads

USER root

RUN echo 'adam ALL=(ALL) NOPASSWD: /usr/bin/python3' >> /etc/sudoers.d/adam

USER adam

COPY user.txt /home/adam/user.txt

USER root
COPY root.txt /root/root.txt

RUN usermod -s /bin/sh www-data