# Cloud_Traccia_1

The app is based on titanic dataset. 
If the file titanic.csv is not in local with path : .\materiale , then it will be downloaded from the [link](https://github.com/awesomedata/awesome-public-datasets/blob/master/Datasets/titanic.csv.zip). 
The root folder has a Dockerfile and a requirements.txt file. The Dockerfile gives the instructions for the docker execution and the requirements.txt file is the list of packages required from the docker to run the app. Bulding the container will take packages and dependences from the requirements.txt file.

## Step 1: Run the main.ipynb notebook 
After this run will be produce a folder named __results__ and a __main.py__ script. Secondly, the notebook will create a docker image named __cloud_titanic__ and from the command or the dashboard you can launch the docker.
In the main.ipynb we define the environment variable with:
_operation = ""
if os.getenv("OPERATION") is not None:
    operation = os.getenv("OPERATION")_

## Step 2: Run the main.py script 
To run the docker container you have to digit:

docker run -e OPERATION=[OPTION] -v "${PWD}/:/home/materiale" cloud_titanic _OPTION_

when the environment variable is set as follows: 

docker run -e OPERATION=print -v "${PWD}/:/home/materiale" cloud_titanic _OPTION_

the results of the function will be printed in the bash shell.

If the environment variable OPERATION is set to another name or if you execute the command without setting any environment variable as follows :

docker run -v "${PWD}/:/home/materiale" cloud_titanic _OPTION_

the data will be plotted and saved in the local .\results repository in .png format.

The options for this app can be:
  * "-survived"
  * "-class"
  * "-age"
  * "-sex_class"

"-survived": Creates the picture with the number of survivors of the titanic

"-class": Creates the picture with the number of passengers divided by class

"-age": Creates the picture with the number of passengers divided by age groups

"-sex_class": Creates the picture of the percentage of survivors by gender and by class

When the docker is launched without any _OPTION_ selected, the result is the list of the selectable metrics.

