import json
from dataclasses import dataclass
from typing import List


@dataclass
class City:
    name: str
    place_id: str
    country_name: str
    country_place_id: str
    country_region: str

    @classmethod
    def from_file(cls, filename) -> List['City']:
        with open(filename, 'r') as file:
            objs = json.loads(file.read())

        return [cls(**obj) for obj in objs]


if __name__ == '__main__':
    cities = City.from_file('cities.json')
