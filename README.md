# Cloud_Traccia_1

The app is based on titanic dataset. The .csv file has been retrieved from https://github.com/awesomedata/awesome-public-datasets/blob/master/Datasets/titanic.csv.zip 
The folder has a Dockerfile and a requirement.txt file. The Dockerfile give the instruction for the docker execution and the requirement.txt file is the list of packages required from the docker to run the app. Bulding the container will take packages and dependances from the requirement.txt file.

## Step 1: Run the main.ipynb notebook
After this run will be produced a folder named titanic and a main.py script. Secondly, the notebook will create a docker image named cloud_titanic and from the command or the dashbboard you can launch the docker.

## Step 2: Launch main.py script 
To launch the main.py script in the docker you have to digit:

python3 main.py <OPTIONS>
  
The options for this app can be:
  *"-?"
  *"-survived"
  *"-class"
  *"-age"
  *"-sex_class"
  
"-?": Lists all possible searchable fields

"-survived": Creates the picture with the number of survivors of the titanic

"-class": Creates the picture with the number of passengers divided by class

"-age": Creates the picture with the number of passengers divided by age groups

"-sex_class": Creates the picture of the percentage of survivors by gender and by class

## Step 3: Open the images created
In the folder ...\Cloud_Traccia_1\titanic, you can open the pictures created previously.
