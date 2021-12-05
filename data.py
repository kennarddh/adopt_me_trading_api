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

        self.ensure_dir('static/images/')

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
                    if not os.path.exists('static/images/{}.png'.format(split_item_data[0])):
                        image = requests.get('{}{}.png'.format(self.image_url, int(split_item_data[0])), stream=True)

                        if image.status_code == 200:
                            with open('static/images/{}.png'.format(split_item_data[0]), 'wb') as file:
                                for chunk in image:
                                    file.write(chunk)
                        else:
                            print('image download failed')

                if onclick.startswith('addPet'):
                    item_data = {
                        'id': int(split_item_data[0]),
                        'name': item.attrs['id'],
                        'is_pet': False,
                        'value': int(split_item_data[1]),
                        'value_neon': 0,
                        'value_mega_neon': 0
                    }
                else:
                    item_data = {
                        'id': int(split_item_data[0]),
                        'name': item.attrs['id'],
                        'is_pet': True,
                        'value': int(split_item_data[1]),
                        'value_neon': int(split_item_data[2]),
                        'value_mega_neon': int(split_item_data[3])
                    }

                data['category'][group_name]['items'][item_name] = item_data

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

        return data

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load(self):
        with open('data.json', 'r') as file:
            return json.load(file)

    def get_raw(self):
        with open('data.json', 'r') as file:
            raw = json.load(file)

        return raw

    def get_all_items(self):
        with open('data.json', 'r') as file:
            all_category = json.load(file)['category']

        all_items = {}

        for category, value in all_category.items():
            for item_name, item_data in value['items'].items():
                all_items[item_name] = item_data

        return all_items

    def get_item_by_id(self, item_id):
        with open('data.json', 'r') as file:
            all_category = json.load(file)['category']

        item = {}

        for category, value in all_category.items():
            for item_name, item_data in value['items'].items():
                if item_data['id'] == int(item_id):
                    item[item_name] = item_data

        return item

    def get_items_by_category(self, category_name):
        with open('data.json', 'r') as file:
            all_category = json.load(file)['category']

        items = {}

        if category_name in all_category.keys():
            items[category_name] = all_category[category_name]

        return items

    def search_item_by_name(self, item_name):
        items = {}

        for category, value in self.load()['category'].items():
            items[category] = {}

            for item_name_loop, item_data in value['items'].items():
                if item_name.lower() in item_data['name'].lower() or item_name.lower() in item_name_loop.lower():
                    items[category][item_name_loop] = item_data

            if items[category] == {}:
                del items[category]

        return items

    def get_image(self, item_id):
        return '{}{}.png'.format(self.image_url, item_id)

if __name__ == '__main__':
    data = Data()

    data.update()
