from django import forms  #https://youtu.be/6oOHlcHkX2U
from .models import Submission, Folder, Code

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
                  'file_name',
                  'code',
                  
                  'CLI_args',
                  'file_name',
                  'stdin'
                  ]
        widgets = {
        'file_name' : forms.Textarea(attrs={'class': 'form-control InputStyle file', 'id':'filename', 'rows':'2', 'cols': '50'}),
            'code': forms.Textarea(attrs={'class': 'form-control', 'id':'code', 'placeholder':'Write your Code here', 'rows': '16', 'cols':'120'}),
            # 'output': forms.Textarea(attrs={'class': 'form-control out', 'placeholder':'The Output will appear here', 'rows':'2'}),
            
            'CLI_args': forms.Textarea(attrs={'rows':'2', 'cols': '50', 'id':'CLI_args'}),
            'stdin': forms.Textarea(attrs={'rows':'2', 'cols': '50', 'id':'stdin'}),
            #'language': forms.Select()
            #'file_name' : forms.CharField(attrs={'class': 'form-control', 'id':'filename'})
        }

class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['code',
                  'language',
                  
                  'stdin',
                  'CLI_args']

        widgets = {
            'code': forms.Textarea(attrs={'class': 'form-control', 'id':'code', 'placeholder':'Write your Code here', 'rows': '16', 'cols':'120'}),
            # 'output': forms.Textarea(attrs={'class': 'form-control out', 'placeholder':'The Output will appear here', 'rows':'2'}),
            'language': forms.Select(),
            
            'CLI_args': forms.Textarea(attrs={'rows':'3', 'cols': '50', 'id':'CLI'}),
            'stdin': forms.Textarea(attrs={'rows':'3', 'cols': '50', 'id':'stdin'}),
        }

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['text', 'language']
        labels = {'text':'Name'}
        widgets = {
                  'language': forms.Select()}
#class FileForm(forms.ModelForm): 
#	class Meta:
#		model = File
#		fields = ['text', 'file_name']
#		labels = {'text': ''}		
#		widgets = {'text': forms.Textarea(attrs={'cols' : 80})}





    
