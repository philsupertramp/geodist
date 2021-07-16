import json
import os
import time
import urllib.parse
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class City:
    name: str
    place_id: str
    country_name: str
    country_place_id: str
    country_region: str
    long: float = 0
    lat: float = 0

    @classmethod
    def from_file(cls, filename) -> List['City']:
        with open(filename, 'r') as file:
            objs = json.loads(file.read())

        return [cls(**obj) for obj in objs]


class PlaceClient:
    def __init__(self):
        self.session = requests.Session()

    def get(self, place_id):
        try:
            return self.session.get(f'https://geocode.xyz/{place_id}?json=1', params={'json': 1})
        except json.decoder.JSONDecodeError as ex:
            print(ex)
            return {}


if __name__ == '__main__':
    cities = City.from_file('cities.json')
    client = PlaceClient()

    prev_iteration = City.from_file('city_coords.json')
    prev_iteration_ids = [i.place_id for i in prev_iteration]

    new_cities = prev_iteration.copy()
    city_count = len(cities)
    prev_count = len(prev_iteration)
    cities = list(filter(lambda x: x.place_id not in prev_iteration_ids, cities))
    error_cities = list()
    for index, city in enumerate(cities):
        out = client.get(urllib.parse.quote(f'{city.name},{city.country_name}'))
        out_json = out.json()
        if not out.ok or out_json.get('error'):
            print(out_json.get('error'))
            print(out.request.url)
            error_cities.append(city.__dict__)
            continue
        city.long = float(out_json.get('longt', 0))
        city.lat = float(out_json.get('latt', 0))
        new_cities.append(city)
        print(f'Processed {prev_count + index+1}/{city_count}: {city.name} in {city.country_name}')
        with open('city_coords.json', 'w') as file:
            file.write(json.dumps([i.__dict__ for i in new_cities]))
        with open('city_coords_failure.json', 'w') as file:
            file.write(json.dumps(error_cities))
        time.sleep(2)
