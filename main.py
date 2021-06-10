#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import seaborn as sns
from datetime import timedelta,date


# In[2]:


#versione di seaborn
sns.__version__


# In[3]:


#CONSIDERIAMO PATH ASSOLUTO (EVENTUALE SVILUPPO CON CRON)
path_abs = str(pathlib.Path().parent.absolute())

#PATH DI DESTINAZIONE DEL MATERIALE GENERATO
path_materiale = str(path_abs+"/titanic/")
file_path = str(path_abs+"/titanic/")


# In[4]:


#print il path del materiale
path_materiale 

#file_path
#path_abs


# In[5]:


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


# In[6]:


#inizializzazione
check_dir(log)

#LETTURA DEL FILE E CREAZIONE DEL DATAFRAME
file = str('titanic.csv')
df = pd.read_csv(file, encoding = "utf-8 ")
df.shape


# In[7]:


df.head(20)


# In[8]:


#Possiamo loggare tutti gli errori da debug in su (info, warning, error e critical)
logging.basicConfig(filename=path_materiale+'main.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


# In[9]:


df['count_survived']=df['Survived'].value_counts()


# In[10]:


df['class_summed']=df['Pclass'].value_counts()


# In[11]:


df['eta_count']= df["Age"].value_counts()


# In[12]:


l_param = []
l_param.append({"value":"-?","desc":"Elenca tutti i possibili campi ricercabili"})
l_param.append({"value":"-survived","desc":"Passeggeri sopravvissuti"})
l_param.append({"value":"-class","desc":"Classe di appertenenza del passeggero"})
l_param.append({"value":"-age","desc":"età dei passeggeri"})
l_param.append({"value":"-sex_class","desc":"percentuale sopravvissuti per sesso e classe "})


def list_parameters():
    print ('LISTA DEI CAMPI A DISPOSIZIONE:\n')
    for i in l_param:
        print("{}\n-- {}\n\n".format(i["value"],i["desc"]))
    
def totale_sopravvissuti(): 
    df['Survived']=np.where(df['Survived']==1 , 'sopravvissuti', 'deceduti')
    fig, ax = plt.subplots(figsize=(8,4))
    titolo = "Numero di passeggeri sopravvissuti"
    plt.title(titolo, fontsize=15)
    plt.xticks(rotation=75)
    plt.barh(df["Survived"],df['count_survived'])
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)

def classe_viaggio(): 
    titolo = "Classe di appartenenza"
    df['prima_classe'] = np.where(df['Pclass']== 1 , 1 , 0)
    df['seconda_classe'] = np.where(df['Pclass']== 2 , 1 , 0)
    df['terza_classe'] = np.where(df['Pclass']== 3 , 1 , 0)
    data = {'prima_classe': int((df['prima_classe']).sum()) , 'seconda_classe': int((df['seconda_classe']).sum()), 'terza_classe': int((df['terza_classe']).sum())}
    names = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(names,values)
    plt.title(titolo, fontsize=15)
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)

def class_sex():
    titolo = "percentuale di sopravvissuti divisi per sesso e classe"
    sns.set_theme(style="whitegrid")
    g = sns.catplot(data=df, kind="bar",x='Sex', y ='Survived' ,  hue="Pclass", palette="dark", alpha=.6, height=6)
    g.despine(left=True)
    g.set_axis_labels("", "% di sopravvissuti per sesso e classe ")
    g.legend.set_title("")
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)

def eta():
    titolo = "età dei passeggeri"   
    df['cat_age']=np.where(df['Age']<10, "0-10", df['Age'])
    df['cat_age']=np.where(((df['Age']<20) & (df['Age']>=10)), "10-20", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<30) & (df['Age']>=20)), "20-30", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<40) & (df['Age']>=30)), "30-40", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<50) & (df['Age']>=40)), "40-50", df['cat_age'])
    df['cat_age']=np.where(df['Age']>=50, ">50", df['cat_age'])
    
    data = {'0-10': int((df['cat_age']=="0-10").sum()) , '10-20': int((df['cat_age']=="10-20").sum()), 
        '20-30': int((df['cat_age']=="20-30").sum()), '30-40': int((df['cat_age']=="30-40").sum()), 
        '40-50': int((df['cat_age']=="40-50").sum()), '>50': int((df['cat_age']==">50").sum())}
    names = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(names,values)
    plt.title(titolo, fontsize=15)
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)


# In[ ]:





# In[13]:


#DA QUI INIZIA IL NOSTRO MAIN, VEDIAMO QUALI SONO I PARAMETRI PASSATI E LANCIAMO LE FUNZIONI CORRISPONDENTI

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
    if command == "-sex_class":
        class_sex()


# In[ ]:





# In[14]:


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




