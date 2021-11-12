import requests
from bs4 import BeautifulSoup

import json
import os
from datetime import datetime


class Data:
    def __init__(self, download_image = True):
        self.request_url = 'https://adoptmetradingvalues.com/'
        self.image_url = 'https://adoptmetradingvalues.com/images/'
        self.download_image = download_image

    def update(self):
        page = requests.get(self.request_url)

        soup = BeautifulSoup(page.content, features='html.parser')

        result = soup.find('div', class_='popupoutergrid').find('div', class_='popupgridcloser').find_all('div', 'popupgrid')

        item_type_list = {
            'animalgrid': 'pets',
            'foodgrid': 'food',
            'vehiclegrid': 'vehicle',
            'petweargrid': 'pet_wear',
            'toygrid': 'toys',
            'strollergrid': 'stroller',
            'giftgrid': 'gift',
            'othergrid': 'other'
        }

        data = {}

        data['last_update'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        data['category_count'] = len(result)

        data['category'] = {}


        for group in result:
            group_name = item_type_list[group.attrs['id']]
            data['category'][group_name] = {}
            data['category'][group_name]['count'] = len(group.find_all('div'))
            data['category'][group_name]['items'] = {}

            for item in group.find_all('div'):
                item_name = '_'.join([i for i in item.attrs['id'].lower().split()])

                onclick = item.attrs['onclick']

                split_item_data = [i.strip() for i in onclick.split('(')[1].split(')')[0].split(',')]

                if self.download_image:
                    if not os.path.exists('images/{}.png'.format(split_item_data[0])):
                        image = requests.get('{}{}.png'.format(self.image_url, int(split_item_data[0])), stream=True)

                        if image.status_code == 200:
                            with open('images/{}.png'.format(split_item_data[0]), 'wb') as file:
                                for chunk in image:
                                    file.write(chunk)
                        else:
                            print('image download failed')

                if onclick.startswith('addPet'):
                    item_data = {
                        'id': int(split_item_data[0]),
                        'name': item.attrs['id'],
                        'value': int(split_item_data[1]),
                        'value_neon': 0,
                        'value_mega_neon': 0
                    }
                else:
                    item_data = {
                        'id': int(split_item_data[0]),
                        'name': item.attrs['id'],
                        'value': int(split_item_data[1]),
                        'value_neon': int(split_item_data[2]),
                        'value_mega_neon': int(split_item_data[3])
                    }

                data['category'][group_name]['items'][item_name] = item_data

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

        return data

    def load(self):
        with open('data.json', 'r') as file:
            return json.load(file)

    def get_image(self, item_id):
        return '{}{}.png'.format(self.image_url, item_id)
