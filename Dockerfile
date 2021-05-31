FROM python:slim-buster
COPY . /home
WORKDIR /home
RUN pip install -r requirements.txt
ENV PROD "True"
#ENTRYPOINT ["python","main.py"]
