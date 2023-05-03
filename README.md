# Nasa Near Earth Object 👨‍🚀🚀

## Installation

### prérequis

- Python 3.2 LTS ou supérieur
- git
- exporter les clés API `SECRET_KEY` et `SECRET_NASA`

`git clone https://github.com/psemsari/NasaNeoTest.git`

Exécuter le fichier `start.sh` ou les commandes ci-dessous

`pip install -r requirements.txt`

`python3 manage.py runserver localhost:8000`
(vous pouvez changer le port par défault)

## Le projet

Ce petit projet permet de connaitre les différents objets près de la Terre entre deux dates données.

Grâce à L'API mise à disposition par la NASA, on peut connaitre le nom, la taille estimé et les différents passages proche de la Terre.

⚠️ L'API de la NASA utilisé est lente, plus il y a de jours plus la page est longue à charger (environ 10 secondes pour un jour donné).

En effet, pour avoir les prochains passages et ancien passages des objets nous devons faire une requête à L'API pour chaque objet de chaque jour et l'API est lente

Une version 2 est disponible sur localhost/v2 mais les informations données sont un peu différentes dû au format de l'api de la NASA

❗ Les deux dates ne doivent pas être différentes de plus de 7 jours

![image](https://user-images.githubusercontent.com/41895689/235939247-eaf9c424-6bd6-44ac-ae36-c2211be2d756.png)
