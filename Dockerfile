FROM python:slim-buster
#COPY . /home
#FROM ubuntu:18.04
#RUN apt update
#RUN apt install -y python3-pip
#RUN pip3 install --upgrade pip
RUN mkdir -p home/materiale
COPY requirements.txt main_2.py /home
WORKDIR /home
RUN pip install -r requirements.txt
RUN rm requirements.txt
ENV PROD "True"


CMD ["-?"]
#ENTRYPOINT ["python","main.py","$OPERATION"]
ENTRYPOINT ["python","main_2.py","$OPERATION"]


