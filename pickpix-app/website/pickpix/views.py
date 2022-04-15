from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template = loader.get_template('pickpix/main.html')
    context = {}
    return HttpResponse(template.render(context, request))
