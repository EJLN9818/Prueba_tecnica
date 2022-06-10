import requests


def get_request_api(request: str):
    response = requests.get('https://restcountries.com/v3.1/' + request)
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        return None

def get_countries():
    return get_request_api('all/')

def get_country_for_name(name:  str):
    return get_request_api(f'name/{name}')
   

def get_countries_for_region(region: str):
    return get_request_api(f'region/{region}')

