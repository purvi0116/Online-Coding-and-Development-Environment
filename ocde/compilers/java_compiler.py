import subprocess
import os
import sys
from subprocess import call    

#MAKE  2 FOLDERS ONE : PROJECT FOLDER OF USER NAMED USING THE ISERNAME OF USE AND 2ND FOLDER CONTAINNING ALL EXTRA FILES THAT U HAVE CREATED AND ARE COPIED TO DOCKER CONTAINER

pwd='purvi2001'

docker_image = "d735a2057e60"

#subprocess.run("docker run -it -m 256M ") ... memory limit not getting set
container_id = subprocess.run("echo {} | sudo -S docker run -it -d ".format(pwd)+docker_image,shell=True, capture_output=True)
#convert to string from byte format
container_id = container_id.stdout.decode()
#truncate the contianer_id by removing the newline character
container_id = container_id[:len(container_id)-2]



project_dir = sys.argv[1]
script_dir = sys.argv[2]
usr_src_code = sys.argv[3]
cli_file = sys.argv[4]
infile = sys.argv[5]
outfile = sys.argv[6]
classfile = usr_src_code[:len(usr_src_code)-5]
username = sys.argv[7]

stdout=""
base_classfile = "/home/"+project_dir[12:]

#copy files from host(i.e. from databse to host and then from host to docker containear) to docker container
subprocess.run("echo {} | sudo -S docker cp ".format(pwd)+project_dir+" "+container_id+":/home" ,shell=True,capture_output=True)
subprocess.run("echo {} | sudo -S docker cp ".format(pwd)+script_dir+" "+container_id+":/home" ,shell=True,capture_output=True)

#delete files from host machine
#subprocess.run("rm -r "+script_dir,shell=True)
#subprocess.run("rm -r "+project_dir,shell=True)

#compile in the docker container
compiled = subprocess.run("echo {} | sudo -S docker exec ".format(pwd)+container_id + " javac -d ./home/"+script_dir[12:]+" ./home/"+project_dir[12:]+usr_src_code,shell=True,capture_output=True)
print(compiled.returncode)




if(compiled.returncode==0):
	timelimit=1
	# display any warnings
	stdout+=compiled.stderr.decode()
	base_classfile = sys.argv[5]
	cli = open(cli_file,"r")
	cli = cli.read()
	execute = subprocess.run("sudo docker exec "+container_id+" bash ./home/"+script_dir[12:]+"/temp_bash.sh "+classfile+" /home/"+infile[12:]+" /home/"+outfile[12:]+" "+str(timelimit)+" "+base_classfile+" "+cli,shell=True,capture_output=True)
	print(execute.returncode)
	print(execute.stdout.decode())
	print(execute.stderr.decode())


else:
	stdout+=compiled.stderr.decode()
	print(compiled.stderr.decode())
	print(compiled.stdout.decode())
	print("CE") 

a = subprocess.run("sudo docker exec "+ container_id+" cat ./home/"+outfile[12:] ,shell=True,capture_output=True)
print(a.returncode)
stdout+=a.stderr.decode()
stdout+=a.stdout.decode()
print("outpput is ",stdout)
outfile=open("./temp_files/"+username+".txt",'a')
outfile.write(stdout)
outfile.close()

#subprocess.run("echo {} | sudo -S docker stop ".format(pwd)+container_id ,shell=True ,capture_output=True)
#subprocess.run("echo {} | sudo -S docker rm ".format(pwd)+container_id ,shell=True, capture_output=True)