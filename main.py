#!/usr/bin/env python
# coding: utf-8

# In[126]:


import pandas as pd
import requests
from collections import defaultdict
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import random
import pathlib 
from pathlib import Path
import sys
import time
import csv
import os
import logging

from datetime import timedelta,date


# In[127]:


#CONSIDERIAMO PATH ASSOLUTO (EVENTUALE SVILUPPO CON CRON)
path_abs = str(pathlib.Path().parent.absolute())
#PATH DI DESTINAZIONE DEL MATERIALE GENERATO
path_materiale = str(path_abs+"/titanic/")
file_path = str(path_abs+"/titanic/")


# In[128]:


path_materiale
#file_path
#path_abs


# In[129]:


#NASCONDERE EVENTUALI WARNING DI PANDAS PER COPIA DEL DF
#pd.options.mode.chained_assignment = None  # default='warn'




#####################################
#CONTROLLO ESISTENZA PERCORSI E FILE
#COLLEZIONO LOG
#####################################
log = []
def check_dir(log):
    if os.path.isdir(path_materiale) == False:
        try: 
            os.mkdir(path_materiale) 
        except OSError as error: 
            log.append({"desc":"Errore nella creazione della directory titanic","code":error})
    else:
        log.append({"desc":"Directory materiale esiste già","code":"0"})


    if os.path.isdir(file_path) == False:
        try: 
            os.mkdir(file_path) 
        except OSError as error:
            log.append({"desc":"Errore nella creazione della directory data","code":error})
    else:
        log.append({"desc":"Directory data esiste già","code":"0"})

#ritorna il filename 
'''def check_file(log):
    filename = ""
    files = os.listdir(file_path)
    for file in files:
        if "csv" in str(file):
            filename = file

    #controllo se esiste il file e in casi lo scarico
    if os.path.isfile(file_path+filename) == False:
        url = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.csv'
        filename = "data_df.csv"
        response = requests.get(url)

        with open(file_path+filename, 'wb') as f:
            for chunk in response.iter_content():
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        
        log.append({"desc":"Scaricata sorgente dati dati da {}".format(url),"code":response})


    else:
        log.append({"desc":"Presente sorgente dati: {}".format(filename),"code":"0"})
    
    return filename'''



##################
#GRAFICI##########
##################
#val_dpi = 300


# '''
# FUNZIONI PER INVIO VERSO CANALE TELEGRAM.
# PRENDE COME ARGOMENTI L'ID DEL CANALE SU CUI INVIARE I MESSAGGI E L'OGGETTO NOTE
# 
# '''
# import telepot
# 
# ###############################
# #SETTAGGI PER BOT TELEGRAM    #
# ###############################
# 
# #ID DEL CANALE SU CUI TRASMETTERE
# id_canale = "-1001191123655"
# #TOKEN DEL BOT (DA CREARE VIA TELEGRAM APP)
# token = '1704955423:AAFOZZysdPZmgfOpSmqW7xr0EcF2bFi3eYw'
# #ISTANZIO IL BOT
# bot = telepot.Bot(token)
# 
# def log_tg(response,extra):
#     msg_id = response["message_id"]
#     msg_date = response["date"]
#     csv_block = []
#     csv_block.append([msg_id,msg_date,extra])
#     with open(path_abs+'/log.csv', 'a+', newline='') as file:
#         writer = csv.writer(file,delimiter=';')
#         writer.writerows(csv_block)
# 
# def remove_old():
#     if os.path.isfile(path_abs+"/log.csv"):
#         new_data = []
#         del_data = {}
#         last_msg_id = 0
# 
#         #COLLEZIONO MESSAGGI DA CANCELLARE
#         with open(path_abs+'/log.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=';')
#             for row in csv_reader:
#                 del_data[int(row[0])] = row
#                 last_msg_id = row[0]
#         if not del_data:
#             return
#         else:
#             print("Preparo la cancellazione msg tg:")
#             first_msg_id = (int(last_msg_id)-110)
#             #NON COMPRENDE I MESSAGGI DI LOCANDA
#             last_msg_id = (int(last_msg_id)+1) 
# 
#             for i in range(int(first_msg_id), int(last_msg_id)):
#                 #print("cancellando messaggio "+ str(i))
#                 response = ""
#                 try:
#                     response = bot.deleteMessage((id_canale,i))
#                 except:
#                     null = 0
#                 else:
#                     data = del_data.get(i, "chiave non presente")
# 
#             #RICREO IL LOG DEI MESSAGGI
#             os.remove(path_abs+"/log.csv")
#             with open(path_abs+'/log.csv', 'w+', newline='') as file:
#                 writer = csv.writer(file,delimiter=';')
#                 for i in new_data:
#                     writer.writerows([i])
#             print("Ricreato indice messaggi tg")
#             
# def send_to_channel(id_canale,obj_note):
#     header = obj_note.get_header()
#     if len(header) == 0:
#         print("Nessun messaggio da inviare")
#         return
#     
#     with open(path_abs+"/sticker/plane.webp", 'rb') as file_toup:
#         response = bot.sendSticker(id_canale, file_toup)
#         log_tg(response,"caricamento sticker")
# 
#         time.sleep(5)
#  
#     
#     for item, content in header.items():
#         msg = content["details"]["msg"]
#         mat_url = path_materiale+content["details"]["mat_url"]
#        
#         
#         #DISTINZIONE TRA TIPO DI DOCUMENTO PER L'INVIO
#         if content["type"] == "img":
#             with open(mat_url, 'rb') as file_toup:
#                 response = bot.sendPhoto(id_canale, file_toup,caption = msg)
#                 log_tg(response,"caricamento immagine")
#                 time.sleep(5)
#         
#         if content["type"] == "doc":
#             with open(mat_url, 'rb') as file_toup:
#                 response = bot.sendDocument(id_canale, file_toup)
#                 log_tg(response,"caricamento documento")
#                 time.sleep(5)
#     
#     response = bot.sendMessage(id_canale,"<i>Aggiornamento completato</i>",parse_mode='HTML' )
#     log_tg(response,"messaggio intro")
# 
# class note(object):
#     def __init__(self):
#         self.header = defaultdict(dict)
#     
#     '''
#     AGGIUNGE UN MESSAGGIO DEFINITO DAI PARAMETRI:
#         ITEM: NOME DEL GRAFICO
#         TIPO: IMG O DOC IN BASE AL TIPO DI DOCUMENTO DA INOLTRARE
#         TESTO: TESTO RAPPRESENTANTE IL FILE DA INOLTRARE
#         MAT_URL: PATH IN CUI SI TROVA IL FILE DA INOLTRARE
#     '''
#     def add_msg(self,item,tipo,testo,url_materiale):    
#         payload = {"msg":testo,"mat_url":url_materiale}
#         self.header[item].update({"type":tipo,"details":payload})
#     
#     '''
#     STAMPA GLI ELEMENTI COLLEZIONATI IN HEADER
#     '''
#     def read(self):
#         for i,j in self.header.items():
#             print("{} {}".format(i,j))
#     
#     '''
#     RESTITUISCE L'OGGETTO HEADER
#     '''
#     def get_header(self):
#         return self.header
# 
#     
# #INSTANZIAMO OGGETTO NOTE
# rel_tg = note()
# 

# In[130]:


#######
# INIT#
#######
check_dir(log)
#filename = check_file(log)
#LETTURA DEL FILE E CREAZIONE DEL DATAFRAME
#file = str(file_path + filename)
file = str('titanic.csv')
df = pd.read_csv(file, encoding = "utf-8 ")
df.shape


# In[131]:


df.head(20)


# In[132]:


#Possiamo loggare tutti gli errori da debug in su (info, warning, error e critical)
logging.basicConfig(filename=path_materiale+'main.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


# In[133]:


#df['count_Survived'] = df['Survived'].count
#df['count_Survived']
#df.loc[df['Survived'] 1, 'count_Survived'] = 


df['count_survived']=df['Survived'].value_counts()


# In[134]:


df['class_summed']=df['Pclass'].value_counts()


# In[135]:


df['eta_count']= df["Age"].value_counts()


# In[136]:


l_param = []
l_param.append({"value":"-?","desc":"Elenca tutti i possibili campi ricercabili"})
l_param.append({"value":"-survived","desc":"Passeggeri sopravvissuti"})
l_param.append({"value":"-class","desc":"Classe di appertenenza del passeggero"})
l_param.append({"value":"-age","desc":"età dei passeggeri"})


def list_parameters():
    print ('LISTA DEI CAMPI A DISPOSIZIONE:\n')
    for i in l_param:
        print("{}\n-- {}\n\n".format(i["value"],i["desc"]))
    
def totale_sopravvissuti(): 
    fig, ax = plt.subplots(figsize=(8,4))
    titolo = "Numero di passeggeri sopravvissuti"
    plt.title(titolo, fontsize=15)
    plt.xticks(rotation=75)
    plt.barh(df["Survived"],df['count_survived'])
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
    #rel_tg.add_msg(filename,"img",titolo,filename)

def classe_viaggio(): 
    titolo = "Classe di appartenenza"
    plt.title(titolo, fontsize=15)
    ax = plt.subplot(111)
    ax.bar(df["prima classe"], df['class_summed'], width=0.5, color='r', align='center')
    ax.bar(df["seconda classe"], df['class_summed'], width=0.5, color='b', align='center')
    ax.bar(df["terza classe"], df['class_summed'], width=0.5, color='r', align='center')
    ax.legend(["prima", "seconda","terza"])
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
    #rel_tg.add_msg(filename,"img",titolo,filename)
    
def eta():
    titolo = "età dei passeggeri"
    plt.title(titolo, fontsize=15)
    ax = plt.subplot(111)
    ax.bar(df["Age"], df["eta_count"], width=0.5, color='r', align='center')
    ax.legend(["età", "frequenza"])
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
    #rel_tg.add_msg(filename,"img",titolo,filename)
    


# In[137]:


#DA QUI INIZIA IL NOSTRO MAIN, VEDIAMO QUALI SONO I PARAMETRI PASSATI E LANCIAMO LE FUNZIONI CORRISPONDENTI
#remove_old()
for i in range(1,len(sys.argv)):
    command = sys.argv[i]
    if command == "-?":
        list_parameters()
        quit()
    if command == "-survived":
        totale_sopravvissuti()
    if command == "-class":
        classe_viaggio()
    if command == "-age":
        eta()


# In[ ]:





# In[ ]:





# In[138]:


#SE NON SIAMO IN PROD CONVERTE IL NOTEBOOK, CANCELLA EVENTUALE BUILD PRECEDENTE E NE CREA UNA NUOVA
if os.getenv("PROD") == None:
    
    command = "jupyter nbconvert --to 'script' main.ipynb"
    os.system(command)
    #stoppo ed elimino eventuali contenitori aperti in modo da poter cancellare e ribuildare l'immagine senza crearne di nuove
    import subprocess
    container_ids = subprocess.check_output(['docker', 'ps', '-aq'], encoding='ascii')
    container_ids = container_ids.strip().split()
    if container_ids:
        subprocess.check_call(['docker', 'stop'] + container_ids)
        subprocess.check_call(['docker', 'rm'] + container_ids)

    command = "docker rmi cloud_titanic"
    os.system(command)

    command = "docker build -t cloud_titanic ."
    os.system(command)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




