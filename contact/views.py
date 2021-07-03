from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, TemplateView

def choose_contact(request):
    return render(request, 'contact/contact.html')
