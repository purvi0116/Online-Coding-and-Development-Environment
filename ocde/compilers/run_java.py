import sys
import subprocess

if __name__ == "__main__":
    try:
        classfile = sys.argv[1] #name of the classfile file in docker container
        input_filename = sys.argv[2] #stdin file
        output_filename = sys.argv[3] #where to output the stdout or stderr
        tl = sys.argv[4] 
        # if block needed???
        base_classfile = sys.argv[5]
        cli = open(sys.argv[5],"r")
        cli = cli.read()

    except IndexError:
        sys.exit(-1)

    input_file = open(input_filename, "r")
    output_file = open(output_filename, "w")   
    sys.exit() 
    execute = subprocess.run("timeout "+ tl+ " java -cp {} {}".format(base_classfile,classfile) + " "+cli,shell=True,capture_output=True,check=True, stdin = input_file)
    rc = execute.returncode
    
    if rc==0:
        output = execute.stdout.decode() 
        output_file.write(output)
        
    elif rc==124:
        output = "TLE"
        output_file.write(output)
    elif rc==136:
        output = "Floating point exception (core dumped)"
        output_file.write(output)
    elif rc==139:
        output = "Segmentation fault (core dumped)"
        output_file.write(output)
    elif rc==134:
        output = "Aborted (core dumped)"
        output_file.write(output)
    elif rc==1:
        output = "Execution failed"
        output += execute.stderr.decode() 
        output_file.write(output)
    elif rc==255:
        output = "Program Timed Out"
        output_file.write(output)      
    else:
        #output=execute.stderr.decode()
        output = "Runtime Error"
        output_file.write(output)

    input_file.close()
    output_file.close()
