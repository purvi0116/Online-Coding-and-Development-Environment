from django.urls import path
from . import views
urlpatterns = [
    path("code_area", views.code_area, name='code_area'),
]
