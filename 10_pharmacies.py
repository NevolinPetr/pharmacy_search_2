import requests
import sys
from full_search import search
from io import BytesIO
from PIL import Image
from pharmacy_search_2 import pharmacies


def main():
    address = " ".join(sys.argv[1:])
    toponym = search(address)
    toponym_coodrinates = ','.join(toponym['Point']['pos'].split())
    response = pharmacies(toponym_coodrinates)
    json_response = response.json()
    organizations = json_response['features'][:10]
    pt = ''
    for i in range(10):
        point = organizations[i]["geometry"]["coordinates"]
        toponym_coodrinates = f'{point[0]},{point[1]}'
        time = organizations[i]["properties"]["CompanyMetaData"]["Hours"]["text"]
        if not time:
            color = 'gr'
        elif time.split(', ')[-1] == 'круглосуточно':
            color = 'bl'
        else:
            color = 'gn'
        pt += f'{toponym_coodrinates},pm2{color}m~'
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    map_params = {
        'l': 'map',
        'pt': pt[:-1]
    }
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()


if __name__ == "__main__":
    main()
