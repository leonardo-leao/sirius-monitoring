# Author: Leonardo Rossi Leao
# E-mail: leonardo.leao@cnpem.br

FROM ubuntu:latest

# Install python
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Setting up Sao Paulo timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends tzdata
RUN rm -rf /var/lib/apt/lists/*
RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Set working directory
WORKDIR /home/app/

# Install python requirements
#RUN python3 -m pip install -r /home/app/requirements.txt

# Running python app
#CMD ["python3", "./main.py"]