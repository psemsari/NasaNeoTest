from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from requests import get, Response
from django.conf import settings
from django import forms

class DatesNeo(forms.Form):
    start = forms.DateField()
    end = forms.DateField()

def index(request: HttpRequest):
    """Return Test of the nasa api"""
    if request.method == 'GET':
        start = '2022-11-08'
        end = '2022-11-09'
        Huston: Response = get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start + '&end_date=' + end + '&api_key=' + settings.SECRET_NASA)
        obj = Huston.json()
        for x in obj['near_earth_objects'][start]:
            print(x['name'], x['id'])
        return (render(request, 'base.html', {'form': DatesNeo()} ))#HttpResponse(Huston.content, content_type="application/json")
    if request.method == 'POST':
        form = DatesNeo(request.POST)
        start = form.data['start']
        Huston: Response = get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start + '&end_date=' + form.data['end'] + '&api_key=' + settings.SECRET_NASA)
        obj = Huston.json()
        dico = obj['near_earth_objects']
        return (render(request, 'base.html', {'form': DatesNeo(), 'obj': dico} ))
