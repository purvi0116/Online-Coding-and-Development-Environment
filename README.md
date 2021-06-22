# Online Coding and Development Environment
### Description
An online code execution system
* Django v3.1.2, PostgreSQL for Database

### Features
* Language Support:
  * Python 3.7.3
  * C++
  * Bash 5.0.3(1)-release
* Users can register and login to thier account to save their work as Code Directory(max 10) containing code files(max 10) of same language
* Support for command line arguments, input via stdin, and time and memory limits
* Sandboxed compilation and execution using Docker
* Detailed execution results
* Allows anyone to run their code without even logging in. But to save work must login.


### Setup
* Install docker for your distribution and create an image named 'gcc' using dockerfile in 'ocde/docker'
  * cd docker
  * docker build -t gcc.
* Install postgres and do the setup
* Create a new database
  * python3 manage.py makemigrations
  * python3 manage.py migrate

