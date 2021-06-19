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


#dichiaro i vari percorsi 
path_abs = str(pathlib.Path().parent.absolute())
path_materiale = "{}/materiale/results/".format(path_abs)
file_path = "{}/materiale/".format(path_abs)


# In[3]:


#definizione var ambiente per decidere output
#se OUT e definita al momento del dockerrun allora la segue, sennò di default non printa nulla
operation = ""
'''
os.environ['OPERATION'] = "print"
os.environ['PROD'] = "print"
'''

if os.getenv("OPERATION") is not None:
    operation = os.getenv("OPERATION")
    


# In[4]:


#non loggo perchè la creo direttamente nel dockerfile
def check_dir(path_materiale):
    #in qualunque caso istanzio il logger
    
    if os.path.isdir(path_materiale) == False:
        try: 
            os.makedirs(path_materiale)
            
        except OSError as error:
            print("error")
    
    #se esiste non loggo nulla
    if os.path.isdir(path_materiale) == True:
        #print("la directory esiste")
        pass


res = check_dir(path_materiale)

logging.basicConfig(handlers=[logging.FileHandler(filename=path_materiale+'filelog.log', encoding='utf-8', mode='a+')],format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


# In[5]:


#####################################
#CONTROLLO ESISTENZA PERCORSI E FILE
#COLLEZIONO LOG
#####################################
#se si trova nella cartella principale lo carico da la e il path è abs sennò lo carico dentro materiale in modo da darlo anche all'utente

file_locale = ""
def down_file(url, filename):
    try:
        logger.info("sto scaricando il file")

        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path+filename, 'wb') as f:
                for chunk in response.iter_content():
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
    
        else:
            logger.info("Errore diverso da 200")

    except Exception as e:
        logger.info("Errore nel scaricare il file")
    
    return file_path+filename


# In[6]:


def check_file():
    file_list = []
    
    #Get the list of all files and directories
    dir_list = os.listdir(file_path)
    file_count = 0
    for file in dir_list:
        if os.path.isfile(file_path+file):
            file_count = file_count+1
    
    #se non ci sono file per forza lo scarico
    if file_count == 0:
        #print("file non trovato lo scarico")
        #se non trovo il file, lo scarico
        url = "https://gist.githubusercontent.com/michhar/2dfd2de0d4f8727f873422c5d959fff5/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv"
        file_list.append({'titanic': down_file(url,"titanic.csv")})
        logger.info("file titanic scaricato")
        return file_list


    #controllo se esiste il un file titanic.csv
    for file in dir_list:
        if os.path.isfile(file_path+file):
            if "csv" and "titanic" in file:
                #print(file)

                logger.info("File titanic trovato in locale")

            #se esiste ritorno il nome del file e abbiamo vinto
                file_list.append({'titanic': "{}/{}".format(file_path,file)}) 
                #print("file trovato")
                return file_list

        


# In[7]:


#vado nel path materiale e seleziono il file
check_dir(path_materiale)
filename = check_file()

#leggo il file csv
file = str(file_path +'titanic.csv')
df = pd.read_csv(file, encoding = "utf-8 ")
logger.info("csv convertito in dataframe")

df['count_survived']=df['Survived'].value_counts()
df['class_summed']=df['Pclass'].value_counts()
df['eta_count']= df["Age"].value_counts()


# In[8]:


l_param = []
l_param.append({"value":"-?","desc":"Elenca tutti i possibili campi ricercabili"})
l_param.append({"value":"-survived","desc":"Passeggeri sopravvissuti"})
l_param.append({"value":"-class","desc":"Classe di appertenenza del passeggero"})
l_param.append({"value":"-age","desc":"età dei passeggeri"})
l_param.append({"value":"-sex_class","desc":"percentuale sopravvissuti per sesso e classe "})

def list_parameters():
    print ('LISTA DELLE METRICHE A DISPOSIZIONE:\n')
    for i in l_param:
        print("{}\n-- {}\n\n".format(i["value"],i["desc"]))

def totale_sopravvissuti(): 
    logger.info("chiamata funzione totale_sopravvissuti")

    df['Survived']=np.where(df['Survived']==1 , 'sopravvissuti', 'deceduti')
    '''fig, ax = plt.subplots(figsize=(8,4))
    titolo = "Passeggeri sopravvissuti"
    plt.title(titolo, fontsize=15)
    plt.xticks(rotation=75)
    plt.barh(df["Survived"],df['count_survived'])
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)'''
    if operation == "print":
        print("sopravvissuti: " + str(df['count_survived'][1]))
        print("non sopravvissuti: " + str(df['count_survived'][0]))
    else:
        fig, ax = plt.subplots(figsize=(8,4))
        titolo = "Passeggeri sopravvissuti"
        plt.title(titolo, fontsize=15)
        plt.xticks(rotation=75)
        plt.barh(df["Survived"],df['count_survived'])
        filename = "{}.png".format(titolo)
        plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
        
    
def classe_viaggio():
    logger.info("chiamata funzione classe_viaggio")
    titolo = "Classe di appartenenza"
    df['prima_classe'] = np.where(df['Pclass']== 1 , 1 , 0)
    df['seconda_classe'] = np.where(df['Pclass']== 2 , 1 , 0)
    df['terza_classe'] = np.where(df['Pclass']== 3 , 1 , 0)
    data = {'prima_classe': int((df['prima_classe']).sum()) , 'seconda_classe': int((df['seconda_classe']).sum()), 'terza_classe': int((df['terza_classe']).sum())}
    '''names = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(names,values)
    plt.title(titolo, fontsize=15)
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)'''
    if operation == "print":
        print("numero di sopravvissuti per classe di biglietto: \n" )
        print(data)
    else:
        names = list(data.keys())
        values = list(data.values())
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(names,values)
        plt.title(titolo, fontsize=15)
        filename = "{}.png".format(titolo)
        plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)

    
def class_sex():
    logger.info("chiamata funzione class_sex")

    titolo = "percentuale_di_sopravvissuti_divisi_per_sesso_e_classe"
    sns.set_theme(style="whitegrid")
    g = sns.catplot(data=df, kind="bar",x='Sex', y ='Survived',  hue="Pclass", palette="dark", alpha=.6, height=6)
    g.despine(left=True)
    g.set_axis_labels("", "% di sopravvissuti per sesso e classe ")
    g.legend.set_title("")
    filename = "{}.png".format(titolo)
    
    #facciamo un try catch perchè catplot si comporta in modo anomalo randomicamente
    
    df['male_first']=np.where((df['Sex']=='male') & (df['Pclass']== 1), 1, 0)
    df['male_second']=np.where((df['Sex']=='male')& (df['Pclass']==2), 1, 0)
    df['male_third']=np.where((df['Sex']=='male')& (df['Pclass']== 3), 1, 0)
    df['female_first']=np.where((df['Sex']=='female')& (df['Pclass']== 1), 1, 0)
    df['female_second']=np.where((df['Sex']=='female')& (df['Pclass']== 2), 1, 0)
    df['female_third']=np.where((df['Sex']=='female')& (df['Pclass']== 3), 1, 0)

    data = {'male-first': int((df['male_first']).sum()) ,
            'male_second': int((df['male_second']).sum()) , 
            'male_third': int((df['male_third']).sum()) ,
            'female_first': int((df['female_first']).sum()) , 
            'female_second': int((df['female_second']).sum()) , 
            'female_third': int((df['female_third']).sum()) }
    
    
    try:
        '''plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
        logger.info("class_sex plot eseguito correttamente")'''
        if operation == "print":
            print("passeggeri divisi per sesso e classe: \n")
            print(data)
        else:
            plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
            logger.info("class_sex plot eseguito correttamente")
            
    except:
        logger.info("class_sex errori nella creazione del catplot")

def eta():
    logger.info("chiamata funzione eta")

    titolo = "eta_dei_passeggeri"   
    df['cat_age']=np.where(df['Age']<10, "0-10", df['Age'])
    df['cat_age']=np.where(((df['Age']<20) & (df['Age']>=10)), "10-20", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<30) & (df['Age']>=20)), "20-30", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<40) & (df['Age']>=30)), "30-40", df['cat_age'])
    df['cat_age']=np.where(((df['Age']<50) & (df['Age']>=40)), "40-50", df['cat_age'])
    df['cat_age']=np.where(df['Age']>=50, ">50", df['cat_age'])
    
    data = {'0-10': int((df['cat_age']=="0-10").sum()) , '10-20': int((df['cat_age']=="10-20").sum()), 
            '20-30': int((df['cat_age']=="20-30").sum()), '30-40': int((df['cat_age']=="30-40").sum()), 
            '40-50': int((df['cat_age']=="40-50").sum()), '>50': int((df['cat_age']==">50").sum())}
    '''names = list(data.keys())
    values = list(data.values())
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(names,values)
    plt.title(titolo, fontsize=15)
    filename = "{}.png".format(titolo)
    plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)'''
    if operation == "print":
        print("eta dei passeggeri: \n" +str(data))
    else:
        names = list(data.keys())
        values = list(data.values())
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(names,values)
        plt.title(titolo, fontsize=15)
        filename = "{}.png".format(titolo)
        plt.savefig(path_materiale+filename,bbox_inches='tight',dpi=300,transparent=False)
        


# In[9]:


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



#SE NON SIAMO IN PROD CONVERTE IL NOTEBOOK, CANCELLA EVENTUALE BUILD PRECEDENTE E NE CREA UNA NUOVA
if os.getenv("PROD") == None:
    command = "jupyter nbconvert --to 'script' main.ipynb"
    os.system(command)
    
    #fermo ed elimino eventuali contenitori aperti in modo da poter cancellare e ribuildare l'immagine senza crearne di nuove
    import subprocess
    container_ids = subprocess.check_output(['docker', 'ps', '-aq'], encoding='ascii')
    container_ids = container_ids.strip().split()
    if container_ids:
        subprocess.check_call(['docker', 'stop'] + container_ids)
        subprocess.check_call(['docker', 'rm'] + container_ids)

    #rimuovo tutte le immagini preesistenti di cloud_titanic        
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




