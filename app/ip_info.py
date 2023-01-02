import requests


def get_info_by_ip(ip: str):
    response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
    data = {
        'ip': response.get('query'),
        'provider': response.get('isp'),
        'org': response.get('org'),
        'country': response.get('country'),
        'region': response.get('regionName'),
        'city': response.get('city'),
        'zip': response.get('zip'),
        'lat': response.get('lat'),
        'lon': response.get('lon'),
    }
    return data
