FROM ubuntu:latest

RUN apt update && apt install  openssh-server sudo -y

RUN useradd -d /home/ubuntu -s /bin/bash -g root -G sudo aboba

RUN  echo 'aboba:Password2018' | chpasswd

RUN service ssh start

CMD ["/usr/sbin/sshd","-D"]