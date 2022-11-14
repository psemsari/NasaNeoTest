from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from requests import get, Response
from django.conf import settings
from django import forms
from django.views.decorators.csrf import csrf_exempt

class DatesNeo(forms.Form):
    start = forms.DateField(input_formats=['%Y-%m-%d'])
    end = forms.DateField(input_formats=['%Y-%m-%d']) #no more than 7 days

def index(request: HttpRequest):
    """Return Test of the nasa api"""

    if request.method == 'GET':
        return (render(request, 'base.html', {'form': DatesNeo()} ))

    if request.method == 'POST':
        form = DatesNeo(request.POST)
        if not form.is_valid():
            return (render(request, 'base.html', {'form': form} ))

        start = form.data['start']
        Huston: Response = get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start + '&end_date=' + form.data['end'] + '&api_key=' + settings.SECRET_NASA)
        if not Huston.status_code == 200:
            return (render(request, 'base.html', {'form': form} ))
        obj = Huston.json()
        dico = obj['near_earth_objects']
        return (render(request, 'base.html', {'form': form, 'obj': dico}))

class IdNeo(forms.Form):
    id = forms.IntegerField()

def moreinfo(request: HttpRequest):
    """Return more info about a Neo"""
    
    if request.method == 'POST':
        form = IdNeo(request.POST)
        if not form.is_valid():
            print(form.errors)
            return (HttpResponse(status=404))

        id = form.data['id']
        Huston: Response = get('https://api.nasa.gov/neo/rest/v1/neo/' + id + '?api_key=' + settings.SECRET_NASA)
        return (HttpResponse(Huston.content))
