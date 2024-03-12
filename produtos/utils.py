

import requests

def make_api_request(url, method='GET', headers=None, params=None, data=None):
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)

        # Verifica se a requisição foi bem-sucedida (código de status 2xx).
        response.raise_for_status()

        return response

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    
def get_attribute(obj, attr):
    return getattr(obj, attr, None)