from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def code_area(request):
    return  HttpResponse("Happy Coding")