from django.urls import path, re_path
from django.conf.urls import include, url
from . import views
#homepage
urlpatterns = [
path('', views.index, name='index'),
#Register
path("register", views.register, name='register'),
#Code_area
path("code_area", views.code_area, name='code_area'),
#Login
path("login", views.login, name='login'),
#Logout
path('logout',views.logout,name='logout'),
#Show all folders
re_path(r'^folders/$', views.folders, name='folders'),
#Show one folder
re_path(r'^folders/(?P<folder_id>\d+)/$', views.folder, name='folder'),
#New folder
re_path(r'^new_folder/$',views.new_folder, name='new_folder'),
path('new_folder2',views.new_folder2,name='new_folder2'),

#To add file to a folder
re_path(r'^new_file/(?P<folder_id>\d+)/$' ,views.new_file, name='new_file'),

#To edit an file of a folder
re_path(r'^edit_file/(?P<file_id>\d+)/$' ,views.edit_file, name='edit_file'),

#To edit a folder
re_path(r'^edit_folder/(?P<folder_id>\d+)/$' ,views.edit_folder, name='edit_folder'),

#To delete a folder
re_path(r'^delete_folder/(?P<folder_id>\d+)/$' ,views.delete_folder, name='delete_folder'),

#To delete a file
re_path(r'^delete_file/(?P<file_id>\d+)/$' ,views.delete_file, name='delete_file'),
]

