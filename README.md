# Cloud_Traccia_1

The app is based on titanic dataset. The titanic.csv file has been retrieved from this [link](https://github.com/awesomedata/awesome-public-datasets/blob/master/Datasets/titanic.csv.zip). 
The root folder has a Dockerfile and a requirements.txt file. The Dockerfile gives the instructions for the docker execution and the requirements.txt file is the list of packages required from the docker to run the app. Bulding the container will take packages and dependences from the requirements.txt file.

## Step 1: Run the main.ipynb notebook 
After this run will be produce a folder named titanic and a main.py script. Secondly, the notebook will create a docker image named cloud_titanic and from the command or the dashboard you can launch the docker.

## Step 2: Run the main.py script 
To run the main.py script in the docker container you have to digit:

python3 main.py _OPTION_ 

The options for this app can be:
  * "-?"
  * "-survived"
  * "-class"
  * "-age"
  * "-sex_class"

"-?": Lists all possible searchable fields

"-survived": Creates the picture with the number of survivors of the titanic

"-class": Creates the picture with the number of passengers divided by class

"-age": Creates the picture with the number of passengers divided by age groups

"-sex_class": Creates the picture of the percentage of survivors by gender and by class

## Step 3: Open the images created
In the folder ...\Cloud_Traccia_1\titanic, you can open the pictures created previously.
