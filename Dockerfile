# Dockerfile, Image, Container
FROM python:3.10
FROM ubuntu:22.04

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip
RUN apt install -y htop
RUN apt install -y wget

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=arm64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Magic happens
RUN apt install -y google-chrome-stable

# Installing Unzip
RUN apt install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`
RUN curl -sS chromedriver.storage.googleapis.com/102.0.5005.27/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Unzip the Chrome Driver into . directory
RUN unzip /tmp/chromedriver.zip chromedriver -d .

# Set display port as an environment variable
ENV DISPLAY=:99

ADD scrape.py .
ADD requirements.txt .

ADD src/__init__.py ./src
#ADD alza.py ./src
ADD src/czc.py ./src
ADD src/items.py ./src
ADD src/mironet.py ./src

RUN pip3 install -r requirements.txt

CMD ["python3", "items.py"]