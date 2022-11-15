from django.shortcuts import render
from django.http import HttpRequest
from requests import get, Response
from django.conf import settings
from django import forms

#afficher son nom, sa taille estimée, la distance à laquelle il passe de la terre et la date de son prochain passage
#Au clic sur un astéroïde, on veut afficher les 5 dernières fois ou l'astéroïde est passé proche de la terre avec
# sa date et la distance à laquelle il est passé

class DatesNeo(forms.Form):
    class Meta:
        labels = {
            's'
        }
    start = forms.DateField(input_formats=['%Y-%m-%d'])
    end = forms.DateField(input_formats=['%Y-%m-%d']) #no more than 7 days

def get_lasts_approachs(object: dict, approachs: list):
    """Retourne la liste des 5 dernières fois où un objet 'object' est passé près de la terre
        Si il n'y en a moins de 5, retourne le restes
    """
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
    """Retourne la date du prochain passage de l'objet 'object' près de la terre
        Si il n'y en a pas, retourne None
    """
    index = approachs.index(object[0])
    lenght = len(approachs)
    if (lenght == index + 1):
        return None
    return approachs[index + 1].get('close_approach_date')

def getmoreinfo(list_object_today: list) -> list:
    """Retourne une liste avec les différentes informations correspondant sur les objets du jour
        Si il y a une erreur avec la requete, retourne None
    """
    resultat = []
    for object in list_object_today:
        requete: Response = get(object.get('links').get('self'))
        if not requete.status_code == 200:
            return (None)
        requete = requete.json()
        resultat.append({
            'name': requete.get('name'),
            'diameter': requete.get('estimated_diameter').get('meters').get('estimated_diameter_max'),
            'distance': object.get('close_approach_data')[0].get('miss_distance').get('kilometers'),
            'next_approach_date': get_next_approach_date(object.get('close_approach_data'), requete.get('close_approach_data')),
            'lasts_approachs': get_lasts_approachs(object.get('close_approach_data'), requete.get('close_approach_data'))
        })
    return resultat

def index(request: HttpRequest):
    """Retourn le rendu de la page"""

    if request.method == 'POST':
        form = DatesNeo(request.POST)

        #Si le formulaire n'est pas valide, on renvend le formulaire avec les erreurs
        if not form.is_valid():
            return (render(request, 'base.html', {'form': form} ))

        start = form.data['start']
        end = form.data['end']

        Houston: Response = get('https://api.nasa.gov/neo/rest/v1/feed?start_date=' + start + '&end_date=' + end + '&api_key=' + settings.SECRET_NASA)
        if not Houston.status_code == 200:
            #houston, on a un problème
            return (render(request, 'base.html', {'form': form, 'error': Houston.json()['error_message']} ))
        
        obj = Houston.json()
        dico: dict = obj['near_earth_objects']
        res = {}
        for date, value in dico.items():
            res.update({date: getmoreinfo(value)})

        return (render(request, 'base.html', {'form': form, 'obj': res}))#HttpResponse(json.dumps(res), content_type='application/json')

    #retourn un formulaire vite pour tout autres types de requêtes
    return (render(request, 'base.html', {'form': DatesNeo()} ))
