import requests

from pytest_yorick.report import attach_yaml


def send_request(request_data):
    if request_data is None:
        raise AttributeError("request_data is None")
    attach_yaml(request_data, 'Request info')
    method = request_data.get('Method', 'GET')
    url = request_data.get('Url', '')
    headers = request_data.get('Headers', {})
    params = request_data.get('Params', {})
    data = request_data.get('Data', {})
    json_data = request_data.get('Json', {})

    if not url:
        raise ValueError("URL is required in request data")

    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=data, json=json_data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, data=data, json=json_data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
