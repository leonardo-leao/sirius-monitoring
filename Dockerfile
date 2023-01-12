# Author: Leonardo Rossi Leao
# E-mail: leonardo.leao@cnpem.br

FROM ubuntu:latest

# Install github
RUN apt-get update && apt-get install -y git

# Install python
RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python3-pip

# Cloning github repository
RUN mkdir /home/app/
WORKDIR /home/app/
RUN git clone https://github.com/leonardo-leao/sirius-monitoring /home/app/

# Setting up environment variables
ENV telegramToken=5285914931:AAFi4G28sWgfH_48f_xPI1zVtoDvS1G6NuY

# Set working directory
WORKDIR /home/app/

RUN python3 -m pip install -r /home/app/requirements.txt
CMD ["python3", "main.py"]