#PARTIAMO DA UNA IMMAGINE CON PYTHON PREINSTALLATO
FROM python:slim-buster
RUN mkdir -p /home/materiale
COPY requirements.txt main.py /home
WORKDIR /home
RUN pip install -r requirements.txt
RUN rm requirements.txt

#PROD SERVE PER EVITARE CHE ALL'INTERNO DEL DOCKER VENGA FATTA LA BUILD
ENV PROD "True"

CMD ["-?"]
#NON UTILIZZIAMO UNA VARIABILE D'AMBIENTE  -E OPERATION DA PASSARE AL MOMENTO DEL DOCKER RUN PERCHÃ¨ UTILIZZIAMO GIÃ  GLI ARGS
#ENTRYPOINT ["python","main.py","$OPERATION"]

#SETTIAMO ENTRY POINT PER FAR ACCETTARE DIRETTAMENTE GLI ARGS AL MOMENTO DEL DOCKER RUN
ENTRYPOINT ["python","main.py"]


