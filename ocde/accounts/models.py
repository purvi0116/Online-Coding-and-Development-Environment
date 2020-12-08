from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class reg_user(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    

LANG_CHOICES = [
    ('Python','Python'),
    ('C++','C++'),
    ('Java','Java'),
    ('Bash','Bash')
]

class Folder(models.Model):
    """Class representing the folder"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    language = models.CharField(max_length=10, choices=LANG_CHOICES, default="c++")
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (("text"),)
    def __str__(self):
        return self.text

class Submission(models.Model):
    """A class to represent the code submission object"""
    file_name = models.CharField(max_length=200)
    code = models.TextField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    CLI = models.BooleanField(default=False)
    CLI_args = models.TextField(blank=True)  #Check out if these have to limited in size, this represents the user input/testcases
    stdin = models.TextField(blank=True)  #Check out if these have to limited in size, this represents the user input/testcases
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'files'
        unique_together = (("file_name"),)
	

class Code(models.Model):
    """A class to represent the code submission object w/o saving option"""
    code = models.TextField()
    stdin = models.TextField(blank=True)  #Check out if these have to limited in size, this represents the user input/testcases
    language = models.CharField(max_length = 10, choices=LANG_CHOICES)
    CLI = models.BooleanField(default=False)
    CLI_args = models.TextField(blank=True)  #Check out if these have to limited in size, this represents the user input/testcases

