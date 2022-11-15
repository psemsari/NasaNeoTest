from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from requests import get, Response
from django.conf import settings
from django import forms
import json

#afficher son nom, sa taille estimée, la distance à laquelle il passe de la terre et la date de son prochain passage
#Au clic sur un astéroïde, on veut afficher les 5 dernières fois ou l'astéroïde est passé proche de la terre avec
# sa date et la distance à laquelle il est passé

class DatesNeo(forms.Form):
    start = forms.DateField(input_formats=['%Y-%m-%d'])
    end = forms.DateField(input_formats=['%Y-%m-%d']) #no more than 7 days

#name, estimates_diameter, close_approche_day(miss_distance.kilometers), close_approche_next(date)
#close_approche_*-5(date, miss_distance.kilometers)

def get_lasts_approachs(object: dict, approachs: list):
    five_lasts = []
    index = approachs.index(object[0])
    if (index <= 5):
        five_lasts = approachs[:index]
    else:
        five_lasts = approachs[(index - 5) : index]
    res = []
    for element in five_lasts:
        res.append({'date': element.get('close_approach_date'), 'distance': element.get('miss_distance').get('kilometers')})
    return res

def get_next_approach_date(object: dict, approachs: list):
    index = approachs.index(object[0])
    lenght = len(approachs)
    if (lenght == index + 1):
        return None
    return approachs[index + 1].get('close_approach_date')

def getmoreinfo(v: list) -> list:
    res = []
    for element in v:
        req: Response = get(element.get('links').get('self'))
        if not req.status_code == 200:
            return (None)
        req = req.json()
        res.append({
            'name': req.get('name'),
            'diameter': req.get('estimated_diameter').get('meters').get('estimated_diameter_max'),
            'distance': element.get('close_approach_data')[0].get('miss_distance').get('kilometers'),
            'next_approach_date': get_next_approach_date(element.get('close_approach_data'), req.get('close_approach_data')),
            'lasts_approachs': get_lasts_approachs(element.get('close_approach_data'), req.get('close_approach_data'))
        })
    return res

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
            return (render(request, 'base.html', {'form': form, 'error': Huston.json()['error_message']} ))
        obj = Huston.json()
        dico: dict = obj['near_earth_objects']
        res = {}
        for k, v in dico.items():
            res.update({k: getmoreinfo(v)})

        return (render(request, 'base.html', {'form': form, 'obj': res}))#HttpResponse(json.dumps(res), content_type='application/json')
