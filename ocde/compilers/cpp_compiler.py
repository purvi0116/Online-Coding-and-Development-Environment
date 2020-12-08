import subprocess
import os
import sys

# system password, the one you enter with sudo ; so as to execute the sudo docker commands
pwd='purvi2001' 

# gcc image for g++
docker_image = "gcc"

# the timelimit makes sure that the user code does not run over the time limit
# it makes use of the standard unix timeout command
timelimit=15
    
# Create a new docker container from the gcc image with memory limit 256 mb so user code does not kill the server; 
# to get the output as container id we redirect any warnings to /dev/null 
container_id = subprocess.run("echo {} | sudo -S docker run -it -d -m 256M ".format(pwd)+docker_image+" 2>/dev/null",shell=True, capture_output=True)
# convert to string from byte format
container_id = container_id.stdout.decode()
# truncate the contianer_id by removing the newline character
container_id = container_id[:len(container_id)-2]

# Use the command line arguments passed for the directory and filenames 
# project_dir folder contains all the source code files of the user... 
# ...(single file in case user wants to run single file and full project if user wants to run the project)
# script dir contains the script file for executing the code and the files for cli, stdin, stdout
project_dir = sys.argv[1]
script_dir = sys.argv[2]
usr_src_code = sys.argv[3]
cli_file = sys.argv[4] 
infile = sys.argv[5]
outfile = sys.argv[6]
username = sys.argv[7]
executable = "/home/"+script_dir[12:]+"/executable"

stdout=""

# copy files from host to docker container
subprocess.run("echo {} | sudo -S docker cp ".format(pwd)+project_dir+" "+container_id+":/home" ,shell=True,capture_output=True)
subprocess.run("echo {} | sudo -S docker cp ".format(pwd)+script_dir+" "+container_id+":/home" ,shell=True,capture_output=True)

# delete files from host machine
subprocess.run("rm -r "+project_dir,shell=True)
subprocess.run("rm -r "+script_dir,shell=True)

# compile cpp code in the docker container
compiled = subprocess.run("echo {} | sudo -S docker exec ".format(pwd)+container_id + " g++ ./home"+project_dir[12:]+usr_src_code+" -lm -o "+executable,shell=True,capture_output=True)


# So this is what happens: if the returncode for the subprocess "compiled" is 0 that means that code compiled successful;
# so we capture any warning messages and then run the python file in the docker conainter for executing the generated executable
# else we copy the compile time error to the stdout file
 
if(compiled.returncode==0):
	# display any warnings
	stdout+=compiled.stderr.decode()
	# call the script to execute the executable
	execute = subprocess.run("sudo docker exec "+container_id+" python3 /home"+script_dir[12:]+"/run_cpp.py "+executable +" "+"/home/"+infile[12:]+" "+"/home/" +outfile[12:]+" "+str(timelimit)+" /home/"+cli_file[12:],shell=True,check=True,capture_output=True
else:
	#copy the compilation error to a file on host machine (uniquely identified by the username)
	stdout = compiled.stderr.decode()
	subprocess.run("rm -f ./temp_files/"+username+".txt",shell=True,capture_output=True)
	subprocess.run("touch ./temp_files/"+username+".txt",shell=True,capture_output=True)
	outfile=open("./temp_files/"+username+".txt",'w')
	outfile.write(stdout)
	outfile.close()
	# stop and delete the docker container
	subprocess.run("echo {} | sudo -S docker stop ".format(pwd)+container_id ,shell=True ,capture_output=True)
	subprocess.run("echo {} | sudo -S docker rm ".format(pwd)+container_id ,shell=True, capture_output=True)
	sys.exit()
	
	
subprocess.run("rm -f ./temp_files/"+username+".txt",shell=True,capture_output=True)
subprocess.run("touch ./temp_files/"+username+".txt",shell=True,capture_output=True)

output = subprocess.run("sudo docker exec "+ container_id+" cat ./home/"+outfile[12:] ,shell=True,capture_output=True)
stdout+=output.stdout.decode()

outfile=open("./temp_files/"+username+".txt",'a')
outfile.write(stdout)
outfile.close()
# stop and delete the docker container
subprocess.run("echo {} | sudo -S docker stop ".format(pwd)+container_id ,shell=True ,capture_output=True)
subprocess.run("echo {} | sudo -S docker rm ".format(pwd)+container_id ,shell=True, capture_output=True)