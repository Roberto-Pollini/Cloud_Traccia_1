#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importo tutto 
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


# dichiaro i vari percorsi 
path_abs = str(pathlib.Path().parent.absolute())
path_materiale = "{}/materiale!!/results!!/".format(path_abs)
file_path = "{}/materiale!!/".format(path_abs)


# In[3]:


#creo le cartelle 
def check_dir(path_materiale):
    print(path_abs)
    if os.path.isdir(path_materiale) == False:
        
        try: 
            os.makedirs(path_materiale)
            print('cartella fatta ')
        except OSError as error:
            print('errore 1 ')
            return(["error",'Errore nella creazione della directory "{}"'.format(path_materiale)])

    if os.path.isdir(path_materiale) == True:
        print('errore 2 ')
        return(["info",'La directory "{}" è stata creata correttamente'.format(path_materiale)])

res = check_dir(path_materiale)


# In[4]:


#####################################
#CONTROLLO ESISTENZA PERCORSI E FILE
#COLLEZIONO LOG
#####################################
#se si trova nella cartella principale lo carico da la e il path è abs sennò lo carico dentro materiale in modo da darlo anche all'utente
file_locale = ""
def down_file(url, filename):
    if "titanic" in filename:
        filename = "titanic.csv"
    
    #logger.info("Non è stato trovato la sorgente {}. Lo sto scaricando dalla rete".format(filename))

    try:
        print('sto scaricando il file' )
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path+filename, 'wb') as f:
                for chunk in response.iter_content():
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            #log.append({"desc":"Scaricata sorgente dati dati da {}".format(url),"code":response})
          #  logger.info("{} è stato scaricato, testo della response: {}".format(filename,response) )
        else:
            print('wertyu')
           # logger.warning("Il sito ha risposto un codice errore diverso da 200 ({})".format(response.status_code))

    except Exception as e:
        print('sdfghj')
       # logger.error("Qualcosa è andato storto nello scaricare {}\n{}".format(filename,e))
    
    return file_path+filename


# In[5]:


def check_file():
    file_list = []
    
    # Get the list of all files and directories
    dir_list = os.listdir(file_path)
    #controlliamo se esistono entrambi i file, sennò scarichiamo
    f_v = f_p = False
    for file in dir_list:
        if "csv" and "titanic" in file:
            f_p = True
            file_list.append({'titanic': "{}/{}".format(file_path,file)}) 
            
              
        
    #se sono presenti entrambi esco e elaboro dalla dir principale       
    if f_p == True:
        print('ce il file' )
       # logger.info("I csv vaccini e titanic sono stati trovati in locale {}".format(file_path))
        return file_list
    
    #li scarico in materiale e li fornisco    
    else:
       # logger.info("Non sono stati trovati entrambi i csv titanic in locale {}".format(file_path))
        file_list = []
        url = "https://gist.githubusercontent.com/michhar/2dfd2de0d4f8727f873422c5d959fff5/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv"
       # logger.info("Scarico il csv titanic da\n{}".format(url))
        file_list.append({'titanic!': down_file(url,"titanic!")})
        print('scarico il file in' + str(file_list))

        
        return file_list


# In[6]:


print('inizio il tutto ')
check_dir(path_materiale)
filename = check_file()



#parte che fa cose 
file = str(file_path +'titanic.csv')
df = pd.read_csv(file, encoding = "utf-8 ")
df.shape

df['count_survived']=df['Survived'].value_counts()
df['class_summed']=df['Pclass'].value_counts()
df['eta_count']= df["Age"].value_counts()


# In[7]:


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
    print(path_materiale)
    print('ciao')
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
    print(titolo)
def class_sex():
    titolo = "percentuale di sopravvissuti divisi per sesso e classe"
    sns.set_theme(style="whitegrid")
    g = sns.catplot(data=df, kind="bar",x='Sex', y ='Survived' ,  hue="Pclass", palette="dark", alpha=.6, height=6)
    g.despine(left=True)
    g.set_axis_labels("", "% di sopravvissuti per sesso e classe ")
    g.legend.set_title("")
    filename = "{}.png".format(titolo)
    try:
        plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
        print('ha printato ')
    except:
        print('non ha scaricato ')
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


# In[8]:


#VEDIAMO QUALI SONO I PARAMETRI PASSATI E LANCIAMO LE FUNZIONI CORRISPONDENTI

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





# In[9]:


#SE NON SIAMO IN PROD CONVERTE IL NOTEBOOK, CANCELLA EVENTUALE BUILD PRECEDENTE E NE CREA UNA NUOVA
if os.getenv("PROD") == None:
    
    command = "jupyter nbconvert --to 'script' main_2.ipynb"
    os.system(command)
    #stoppo ed elimino eventuali contenitori aperti in modo da poter cancellare e ribuildare l'immagine senza crearne di nuove
    import subprocess
    container_ids = subprocess.check_output(['docker', 'ps', '-aq'], encoding='ascii')
    container_ids = container_ids.strip().split()
    if container_ids:
        subprocess.check_call(['docker', 'stop'] + container_ids)
        subprocess.check_call(['docker', 'rm'] + container_ids)

### rimuovo tutte le immagini preesistenti di cloud_titanic        
    command = "docker rmi cloud_titanic"
    os.system(command)
    
    #command = "docker run -e OPERATION = command -v cloud_titanic"
    #os.system(command)
    
    #command = "docker run -v $(PWD) -e DATASET= titanic.csv"
    #os.system(command)
    #command = ""
#creo la mia immagine 


    command = "docker build -t cloud_titanic ."
    os.system(command)

    #command = "docker run -it --entrypoint /bin/bash cloud_titanic"
    #command = "docker run -it cloud_titanic ."
    #os.system(command)
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




