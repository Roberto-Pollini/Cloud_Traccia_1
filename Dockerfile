FROM python:slim-buster
COPY . /home
#COPY main.py requirements.txt /home
WORKDIR /home
RUN pip install -r requirements.txt
#RUN rm requirements.txt
ENV PROD "True"
#CMD ["-?"]
#ENTRYPOINT ["python","main.py","$OPERATION"]
ENTRYPOINT ["python","main_2.py","$OPERATION"]


