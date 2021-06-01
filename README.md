# Cloud_Traccia_1

The app is based on titanic dataset. The .csv file has been retrieved from "inserire il link"
The folder has a Dockerfile and a requirement.txt file. The Dockerfile give the instruction for the docker execution and the requirement.txt file is the list of packages required from the docker to run the app. Bulding the container will take packages and dependances from the .txt file.

Run the main.ipynb notebook, this step will produce a folder ( titanic) and a main.py script. Secondly the notebook will create a docker image and from the command or the dashbboard you can launch the docker.

To launch the main.py script in the docker you have to digit:

python3 main.py <OPTIONS>
  
  where options could be:
  "-?"
  "-survived"
  "-age"
  "etx...."
  
  to get respectively metrics from dataset...
