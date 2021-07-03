from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, TemplateView

def choose_about(request):
    return render(request, 'about/about.html')
