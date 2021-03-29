import os
import pygame
import requests
import sys
from distance import lonlat_distance
from full_search import search


def pharmacies(coodrinates):
    search_api_server = 'https://search-maps.yandex.ru/v1/'
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    search_params = {
        'apikey': api_key,
        'text': 'аптека',
        'lang': 'ru_RU',
        'll': coodrinates,
        'type': 'biz'
    }
    return requests.get(search_api_server, params=search_params)


def main():
    address = " ".join(sys.argv[1:])
    toponym = search(address)
    toponym_coodrinates = ','.join(toponym['Point']['pos'].split())
    response = pharmacies(toponym_coodrinates)
    json_response = response.json()
    organization = json_response['features'][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    org_point = f'{point[0]},{point[1]}'
    time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    dist = int(lonlat_distance(list(map(float, toponym_coodrinates.split(','))), [float(point[0]), float(point[1])]))
    snippet = f'адрес: {org_address}', f'название аптеки: {org_name}', f'время работы: {time}', f'расстояние: {dist}м'
    map_params = {
        'l': 'map',
        'pt': f'{toponym_coodrinates},pm2am~{org_point},pm2bm'
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    pharmacy = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(pharmacy.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    font = pygame.font.Font(None, 20)
    for i in range(len(snippet)):
        text = font.render(snippet[i], True, (0, 0, 255))
        text_x = 10
        text_y = 10 + text.get_height() * i
        screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
