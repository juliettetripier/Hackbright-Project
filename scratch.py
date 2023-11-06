import os
import requests

YELP_API_KEY = os.environ['YELP_KEY']

def get_restaurant_info(yelp_id):
    url = f'https://api.yelp.com/v3/businesses/{yelp_id}'
    payload = {
        'id': yelp_id
    }
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {YELP_API_KEY}',
    }

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    restaurant_dict = {'address': " ".join(data['location']['display_address']), 'res_name':data['name'],
                       'yelp_id': yelp_id}

    return restaurant_dict


get_restaurant_info('kdTFcDSl9vAR-btEm1Q2uw')