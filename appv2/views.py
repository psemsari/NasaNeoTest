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

def getmoreinfo(list_object_today: list) -> list:
    """Retourne une liste avec les différentes informations correspondant sur les objets du jour
        Si il y a une erreur avec la requete, retourne None
    """
    resultat = []
    for object in list_object_today:
        resultat.append({
            'name': object.get('name'),
            'diameter': object.get('estimated_diameter').get('meters').get('estimated_diameter_max'),
            'distance': object.get('close_approach_data')[0].get('miss_distance').get('kilometers'),
            'id': object.get('id')
        })
    return resultat

def index(request: HttpRequest):
    """Retourn le rendu de la page"""
    if request.method == 'POST':
        form = DatesNeo(request.POST)

        #Si le formulaire n'est pas valide, on renvend le formulaire avec les erreurs
        if not form.is_valid():
            return (render(request, 'basev2.html', {'form': form} ))

        start = form.data['start']
        end = form.data['end']

        Houston: Response = get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start + '&end_date=' + end + '&api_key=' + settings.SECRET_NASA)
        if not Houston.status_code == 200:
            #houston, on a un problème
            return (render(request, 'basev2.html', {'form': form, 'error': "erreur de requête"} ))
        obj = Houston.json()
        dico: dict = obj['near_earth_objects']
        res = {}
        for date, value in dico.items():
            res.update({date: getmoreinfo(value)})

        return (render(request, 'basev2.html', {'form': form, 'obj': res}))#HttpResponse(json.dumps(res), content_type='application/json')

    #retourn un formulaire vite pour tout autres types de requêtes
    return (render(request, 'basev2.html', {'form': DatesNeo()} ))

def get_lasts_approachs(index, approachs):
    """Retourne la liste des 5 dernières fois où un objet 'object' est passé près de la terre
        Si il n'y en a moins de 5, retourne le restes
    """
    five_lasts = []
    if (index <= 5):
        five_lasts = approachs[:index]
    else:
        five_lasts = approachs[(index - 5) : index]
    res = []
    for element in five_lasts:
        res.append({'date': element.get('close_approach_date'), 'distance': element.get('miss_distance').get('kilometers')})
    return res

def get_next_approach_date(index, approachs):
    """Retourne la date du prochain passage de l'objet 'object' près de la terre
        Si il n'y en a pas, retourne None
    """
    lenght = len(approachs)
    if (lenght == index + 1):
        return None
    return approachs[index + 1].get('close_approach_date')


def get_index_approachs_by_date(list_approachs: list, search_date):
    for index, element in enumerate(list_approachs):
        if (element.get('close_approach_date') == search_date):
            return index
    return 0

class IdNeo(forms.Form):
    id = forms.IntegerField()
    date = forms.DateField(input_formats=['%Y-%m-%d'])

def moreinfo(request: HttpRequest):
    """Retourne plus d'info sur un objet selon sa date et son id (envoyé par le client)"""
    if request.method == 'POST':
        form = IdNeo(request.POST)
        if not form.is_valid():
            return (HttpResponse(status=404))

        id = form.data['id']
        date = form.data['date']
        requete: Response = get('https://api.nasa.gov/neo/rest/v1/neo/' + id + '?api_key=' + settings.SECRET_NASA)
        if not requete.status_code == 200:
            return (HttpResponse(status=404))
        requete = requete.json()
        list_approachs = requete.get('close_approach_data')
        index = get_index_approachs_by_date(list_approachs, date)
        resultat = {
            'next_approach_date': get_next_approach_date(index, list_approachs),
            'lasts_approachs': get_lasts_approachs(index, list_approachs)
        }
        return (HttpResponse(json.dumps(resultat), content_type='application/json'))
    return (HttpResponse(status=403))
