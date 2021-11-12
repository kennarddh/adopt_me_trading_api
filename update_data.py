import requests
import json
import os
from bs4 import BeautifulSoup


request_url = 'https://adoptmetradingvalues.com/'
image_url = 'https://adoptmetradingvalues.com/images/'
download_image = True

page = requests.get(request_url)

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

data['items'] = {}

for group in result:
    group_name = item_type_list[group.attrs['id']]
    data['items'][group_name] = {}

    for item in group.find_all('div'):
        item_name = '_'.join([i for i in item.attrs['id'].lower().split()])

        onclick = item.attrs['onclick']

        split_item_data = [i.strip() for i in onclick.split('(')[1].split(')')[0].split(',')]

        if download_image:
            if not os.path.exists('images/{}.png'.format(split_item_data[0])):
                image = requests.get('{}{}.png'.format(image_url, int(split_item_data[0])), stream=True)

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

        data['items'][group_name][item_name] = item_data

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
