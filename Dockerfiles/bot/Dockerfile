# Author: Leonardo Rossi Leao
# E-mail: leonardo.leao@cnpem.br

FROM python:3.9-alpine

# Set working directory
WORKDIR /home/app/

# Install python requirements
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Running python monitor app
CMD ["python", "./bot.py"]