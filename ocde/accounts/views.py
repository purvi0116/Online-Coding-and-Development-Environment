from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Folder, Submission
from .forms import FolderForm,SubmissionForm,CodeForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import subprocess
import random
import string, secrets



num_folders = 0
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('folders')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'login.html')
    else:
       return render(request, 'login.html') 
#def register(request):
#    return render(request, 'register.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user_created')
                return redirect('login')
        else:
            print('password not matching')
        return render(request, 'register.html')
    else:
        return render(request, 'register.html')
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def code_area(request):
    stdout = ""
    file = open("temp.json", 'r')
    pre_code = file.read()
    #print(pre_code)
    file.close()
    if (request.method!='POST'):  
        form = CodeForm()
        

    else:
        
        N=5
        username = res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                  for i in range(N)) 
        username = str(username)
        form = CodeForm(request.POST)
        lang = form.data['language']
        #letters = string.ascii_lowercase
        #username = str(''.join(random.choice(letters)) for i in range(5))
        if form.is_valid():
            cli=""
            cli = request.POST["CLI_args"]
            stdin=""
            stdin=request.POST["stdin"]
            
            if(lang=="C++"):
                src_codefile = "main.cpp"        
            elif(lang=="Python"):
                src_codefile = "main.py"
            elif(lang=="Bash"):
                src_codefile = "main.sh"                

            if '_run' in request.POST or '_runProject' in request.POST:
                print("run")
                code = form.data['code']
                
                base="./temp_files/"
                # create the input file 
                project_dir = username+"/"
                script_dir = username+"_dir"
                subprocess.run("rm -rf "+base+script_dir,shell=True)
                subprocess.run("mkdir "+base+script_dir,shell=True)
                subprocess.run("rm -rf "+base+project_dir,shell=True)
                subprocess.run("mkdir "+base+project_dir,shell=True)
                infile = base+script_dir+"/"+username+"_in.txt"
                outfile = base+script_dir+"/"+username+"_out.txt"
                cli_file = base+script_dir+"/"+username+"_cli.txt"
                subprocess.run("touch "+infile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+cli_file,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+outfile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+base+project_dir+src_codefile,shell = True) # required only if some text input on stdin is given
                subprocess.run("echo "+stdin+" > "+infile,shell = True)
                #subprocess.run('echo '+code+' > '+base+project_dir+src_codefile,shell = True)
                
                file_code = open(base+project_dir+src_codefile, 'w')
                file_code.write(code)
                file_code.close()

                if lang=="C++":
                    subprocess.run("cp ./compilers/run_cpp.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/cpp_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Python":
                    subprocess.run("cp ./compilers/run_py.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/python_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                    print(stdout.returncode)
                elif lang=="Java":
                    subprocess.run("cp ./compilers/subprocess.sh "+base+script_dir,shell=True)
                    subprocess.run("cp ./compilers/temp_bash.sh "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    subprocess.run("python3 ./compilers/java_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Bash":
                    subprocess.run("cp ./compilers/run_bash.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    print(cli_subprocess)
                    stdout=subprocess.run("python3 ./compilers/bash_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                    print(stdout.returncode)
                stdoutFile = open("./temp_files/"+username+".txt",'r')
                stdout = stdoutFile.read()
                stdoutFile.close()
                subprocess.run("rm -f "+"./temp_files/"+username+".txt",shell=True)
                print(stdout)
            elif '_stop' in request.POST:
                print("stop")
            elif '_save' in request.POST:
                messages.info(request,'To save your work first create a folder and then a file')
                folders = Folder.objects.filter(owner=request.user).order_by('date_added')[:10]
                context={'folders':folders}
                return render(request, 'folders.html',context)

            context={'form':form, 'stdout':'\n'+stdout}
            #return HttpResponseRedirect('/code_area',context)  
            return render(request,'code_area.html',context)
            #new
    context = {
        'form' : form,
        'stdout':stdout
    }
    return render(request, 'code_area.html',context)

@login_required
def folders(request):
    if Folder.objects.filter(owner=request.user).count()>10:
        messages.info(request,'Folder Limit Exceeded')
        folders = Folder.objects.filter(owner=request.user).order_by('date_added')[:10]
        message = "Folder Limit Exceeded"
        context={'folders':folders, 'message':message}
        return render(request,'folders.html',context)	
    else:
        folders = Folder.objects.filter(owner=request.user).order_by('date_added')[:10]
        context={'folders':folders}
        return render(request,'folders.html',context)	

@login_required
def folder(request, folder_id):
	"""Show a single topic and all its entries"""
	folder = Folder.objects.get(id=folder_id)
	#Make sure theat the folder belongs to the current owner
	check_folder_owner(request, folder)
	files = folder.submission_set.order_by('-date_added')
	context = {'folder':folder,'files':files}
	return render(request,'folder.html',context)	

@login_required
def new_folder(request):
    if Folder.objects.filter(owner=request.user).count() <= 10 :
        if request.method=='POST':
            folder=request.POST['folder']
            folder_obj = Folder(text=folder)
            folder_obj.save()
            return HttpResponseRedirect('/folders')
        return render(request,'new_folder.html')
    else:
        messages.info(request,'Folder Limit Exceeded')
        return render(request,'new_folder.html')
        #return HttpResponseRedirect('/folders')	

@login_required
def new_folder2(request):
	"""Add a new folder."""
	if request.method!='POST':
		#No data submitted;create a blank form.
		form = FolderForm()
	else:
		#POST data submitted; process data
		form = FolderForm(request.POST)
		if form.is_valid():
			new_folder = form.save(commit=False)
			new_folder.owner = request.user
			new_folder.save()
			return HttpResponseRedirect('/folders')	
	context = {'form' : form}
	return render(request,'new_folder2.html',context)		

@login_required
def new_file(request,folder_id):
    folder = Folder.objects.get(id=folder_id)
    lang = folder.language
    check_folder_owner(request,folder)
    stdout=""
    if request.method!='POST': 
        form = SubmissionForm()
    else:
        form = SubmissionForm(request.POST)
        username = str(request.user)
        if form.is_valid():
            if '_save' in request.POST:
                new_file = form.save(commit=False)	
                new_file.folder = folder
                new_file.save()
                return HttpResponseRedirect('/folders/'+folder_id)
            elif '_run' in request.POST or '_runProject' in request.POST:
                #get code,code filename, cli args, stdin from POST request
                code = request.POST["code"]
                cli = request.POST["CLI_args"]
                stdin=request.POST["stdin"]
                src_codefile = request.POST["file_name"] 
                
                base="./temp_files/"
                # create the input file 
                project_dir = username+"_code/"
                script_dir = username+"_dir"
                subprocess.run("rm -rf "+base+script_dir,shell=True)
                subprocess.run("mkdir "+base+script_dir,shell=True)
                subprocess.run("rm -rf "+base+project_dir,shell=True)
                subprocess.run("mkdir "+base+project_dir,shell=True)
                infile = base+script_dir+"/"+username+"_in.txt"
                outfile = base+script_dir+"/"+username+"_out.txt"
                cli_file = base+script_dir+"/"+username+"_cli.txt"
                subprocess.run("touch "+infile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+cli_file,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+outfile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+base+project_dir+src_codefile,shell = True) # required only if some text input on stdin is given
                subprocess.run("echo "+stdin+" > "+infile,shell = True)
    
                file_code = open(base+project_dir+src_codefile, 'w')
                file_code.write(code)
                file_code.close()
                if '_runProject' in request.POST:
                    files = Submission.objects.filter(folder=folder)
                    for i in range(0,len(files)):
                        if(str(files[i].id)==str(file_id)):
                            continue
                        else:
                            src_code=str(files[i].code)    
                            filename = str(files[i].file_name)
                            file_code = open(base+project_dir+filename, 'w')
                            file_code.write(src_code)
                            file_code.close()

                if lang=="C++":
                    subprocess.run("cp ./compilers/run_cpp.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/cpp_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Python":
                    subprocess.run("cp ./compilers/run_py.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/python_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Java":
                    subprocess.run("cp ./compilers/subprocess.sh "+base+script_dir,shell=True)
                    subprocess.run("cp ./compilers/temp_bash.sh "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    subprocess.run("python3 ./compilers/java_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Bash":
                    subprocess.run("cp ./compilers/run_bash.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/bash_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                stdoutFile = open("./temp_files/"+username+".txt",'r')
                stdout = '\n'+stdoutFile.read()
                stdoutFile.close()
                subprocess.run("rm -f "+"./temp_files/"+username+".txt",shell=True)

            elif '_stop' in request.POST:
                stdout=""
            
    callBack_url = '/new_file/'+folder_id+'/'		
    context = {'folder': folder, 'form': form, 'callBack_url':callBack_url, 'stdout':stdout}
    return render(request, 'new_file.html',context)		

@login_required
def edit_file(request,file_id):
    file = Submission.objects.get(id=file_id)
    folder = file.folder
    lang = folder.language # pick the language from the folder selected
    check_folder_owner(request,folder)
    stdout="" # blank if get request
    if request.method!='POST':
        # Initial request; pre-fill form with the current entry.
        form =  SubmissionForm(instance=file)
    else:
        # POST data submitted; process data.
        username=request.user.username
        form = SubmissionForm(instance=file, data=request.POST)
        if form.is_valid():       
            if '_save' in request.POST:
                form.save()
                return HttpResponseRedirect('/folders/'+str(folder.id)+'/') 
            elif '_run' in request.POST or '_runProject' in request.POST:
                #get code,code filename, cli args, stdin from POST request
                code = file.code
                cli = request.POST["CLI_args"]
                stdin=request.POST["stdin"]
                src_codefile = request.POST["file_name"] 
                
                base="./temp_files/"
                # create the input file 
                project_dir = username+"_code/"
                script_dir = username+"_dir"
                subprocess.run("rm -rf "+base+script_dir,shell=True)
                subprocess.run("mkdir "+base+script_dir,shell=True)
                subprocess.run("rm -rf "+base+project_dir,shell=True)
                subprocess.run("mkdir "+base+project_dir,shell=True)
                infile = base+script_dir+"/"+username+"_in.txt"
                outfile = base+script_dir+"/"+username+"_out.txt"
                cli_file = base+script_dir+"/"+username+"_cli.txt"
                subprocess.run("touch "+infile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+cli_file,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+outfile,shell = True) # required only if some text input on stdin is given
                subprocess.run("touch "+base+project_dir+src_codefile,shell = True) # required only if some text input on stdin is given
                subprocess.run("echo "+stdin+" > "+infile,shell = True)
    
                file_code = open(base+project_dir+src_codefile, 'w')
                file_code.write(code)
                file_code.close()
                if '_runProject' in request.POST:
                    files = Submission.objects.filter(folder=folder)
                    for i in range(0,len(files)):
                        if(str(files[i].id)==str(file_id)):
                            continue
                        else:
                            src_code=str(files[i].code)    
                            filename = str(files[i].file_name)
                            file_code = open(base+project_dir+filename, 'w')
                            file_code.write(src_code)
                            file_code.close()

                if lang=="C++":
                    subprocess.run("cp ./compilers/run_cpp.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/cpp_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Python":
                    subprocess.run("cp ./compilers/run_py.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/python_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Java":
                    subprocess.run("cp ./compilers/subprocess.sh "+base+script_dir,shell=True)
                    subprocess.run("cp ./compilers/temp_bash.sh "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    subprocess.run("python3 ./compilers/java_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                elif lang=="Bash":
                    subprocess.run("cp ./compilers/run_bash.py "+base+script_dir,shell=True)
                    cli_subprocess = src_codefile+" "+cli_file+" "+infile+" "+outfile+" "+username
                    stdout=subprocess.run("python3 ./compilers/bash_compiler.py "+base+project_dir+" "+base+script_dir+" "+cli_subprocess,shell=True)
                stdoutFile = open("./temp_files/"+username+".txt",'r')
                stdout = '\n'+stdoutFile.read()
                stdoutFile.close()
                subprocess.run("rm -f "+"./temp_files/"+username+".txt",shell=True)

            elif '_stop' in request.POST:
                stdout=""
            #new
            
            context={'form':form, 'folder':folder, 'file':file,'stdout':stdout}
            #return HttpResponseRedirect('/code_area',context)  
            return render(request,'edit_file.html',context)
                
    context={'form':form, 'folder':folder, 'file':file,'stdout':stdout}
    return render(request,'edit_file.html',context) 

@login_required
def edit_folder(request,folder_id):
	"""Edit an existing entry"""
	folder = Folder.objects.get(id=folder_id)
	check_folder_owner(request,folder)
	if request.method!='POST':
		# Initial request; pre-fill form with the current topic.
		form = 	FolderForm(instance=folder)
	else:
		# POST data submitted; process data.
		form = FolderForm(instance=folder, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/folders/')	
	context={'form':form, 'folder':folder}
	return render(request,'edit_folder.html',context)	

@login_required
def delete_folder(request, folder_id):
	folder = Folder.objects.get(id=folder_id)
	check_folder_owner(request, folder)
	folder.delete()
	return HttpResponseRedirect('/folders/')	

@login_required
def delete_file(request, file_id):
	file = Submission.objects.get(id=file_id)
	folder = file.folder
	check_folder_owner(request, folder)
	file.delete()
	folder_id = folder.id
	return HttpResponseRedirect('/folders/'+str(folder_id)+'/')

def check_folder_owner(request,folder):
	if folder.owner!=request.user:
		raise Http404	

def create_files(username):
    base="./temp_files/"
    # create the input file 
    project_dir = username+"_code/"
    script_dir = username+"_dir"
    subprocess.run("rm -rf "+base+script_dir,shell=True)
    subprocess.run("mkdir "+base+script_dir,shell=True)
    subprocess.run("rm -rf "+base+project_dir,shell=True)
    subprocess.run("mkdir "+base+project_dir,shell=True)
    infile = base+script_dir+"/"+username+"_in.txt"
    outfile = base+script_dir+"/"+username+"_out.txt"
    cli_file = base+script_dir+"/"+username+"_cli.txt"
    subprocess.run("touch "+infile,shell = True) # required only if some text input on stdin is given
    subprocess.run("touch "+cli_file,shell = True) # required only if some text input on stdin is given
    subprocess.run("touch "+outfile,shell = True) # required only if some text input on stdin is given
    subprocess.run("touch "+base+project_dir+src_codefile,shell = True) # required only if some text input on stdin is given
    subprocess.run("echo "+stdin+" > "+infile,shell = True)