import sys
from io import BytesIO
import requests
from PIL import Image
from spn import find_spn


def search(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


toponym = search(" ".join(sys.argv[1:]))
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split()
env = toponym['boundedBy']['Envelope']
lc = toponym['boundedBy']['Envelope']['lowerCorner'].split()
uc = toponym['boundedBy']['Envelope']['upperCorner'].split()
spn = find_spn(toponym)
pt = toponym_longitude + ',' + toponym_lattitude + ',pmrdm'
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(spn),
    "l": "map",
    'pt': pt
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()
