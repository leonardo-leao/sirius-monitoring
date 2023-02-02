# Author: Leonardo Rossi Leao
# E-mail: leonardo.leao@cnpem.br

FROM python:3.9-alpine

# Set working directory
WORKDIR /home/app/

# Install python requirements
RUN pip3 install -r requirements.txt

# Running python monitor app
CMD ["python", "./bot.py"]