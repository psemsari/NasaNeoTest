![image](https://img.shields.io/badge/Maintained%3F-no-red.svg)

# Nasa Near Earth Object 👨‍🚀🚀

## The Project

This small project allows to know the different objects near the Earth between two given dates.

Thanks to the API provided by NASA, we can know the name, the estimated size and the different passages near the Earth.

⚠️ The NASA API used is slow, the more days there are the longer the page takes to load (about 10 seconds for a given day).

Indeed, to have the next passages and old passages of the objects we must make a request to the API for each object of each day and the API is slow

A version 2 is available on localhost/v2 but the information given is a little bit different due to the format of the NASA api

❗ The two dates must not be different of more than 7 days

![image](https://user-images.githubusercontent.com/41895689/235939247-eaf9c424-6bd6-44ac-ae36-c2211be2d756.png)

## Installation

### prerequisites

- Python 3.2 LTS or higher
- git
- export the API keys SECRET_KEY and SECRET_NASA

`git clone https://github.com/psemsari/NasaNeoTest.git`

Run the start.sh file or the commands below

`pip install -r requirements.txt`

`python3 manage.py runserver localhost:8000`
(you can change the default port)
