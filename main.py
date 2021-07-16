import json

import requests as requests


class CityClient:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get(self):
        count = self.session.get(self.url).json()['count']
        count += 100  # just add some on top for the range
        result = list()
        for iteration in range(0, count, 200):
            result += self.session.get(self.url + f'?limit=200&offset={iteration}').json()['results']
        return result

    @staticmethod
    def clean(objs):
        return [
            {
                'name': obj.get('name'),
                'place_id': obj.get('place_id'),
                'country_name': obj.get('country').get('name') if obj.get('country') else None,
                'country_place_id': obj.get('country').get('place_id') if obj.get('country') else None,
                'country_region': obj.get('country').get('region') if obj.get('country') else None,
            } for obj in objs
        ]


if __name__ == '__main__':
    client = CityClient('https://api.moberries.com/api/v2/cities/')

    with open('cities.json', 'r') as file:
        with open('cities.json', 'w') as out_file:
            out_file.write(json.dumps(client.clean(json.loads(file.read()))))

