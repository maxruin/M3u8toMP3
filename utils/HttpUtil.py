import requests

def post(url, params):
    """
    Sends a POST request to the specified URL with the given parameters.

    :param url: The URL to send the POST request to.
    :param params: A dictionary of parameters to include in the POST request.
    :return: The response from the server.
    """
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def post_json(url, params):
    """
    Sends a POST request to the specified URL with the given parameters.

    :param url: The URL to send the POST request to.
    :param params: A dictionary of parameters to include in the POST request.
    :return: The response from the server.
    """
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
        
def get_with_bearer(url, bearer_token):
    """
    Sends a GET request to the specified URL with the given Bearer token.

    :param url: The URL to send the GET request to.
    :param bearer_token: The Bearer token for authorization.
    :return: The response from the server.
    """
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def post_with_bearer(url, params, bearer_token):
    """
    Sends a POST request to the specified URL with the given parameters and Bearer token.

    :param url: The URL to send the POST request to.
    :param params: A dictionary of parameters to include in the POST request.
    :param bearer_token: The Bearer token for authorization.
    :return: The response from the server.
    """
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(url, data=params, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None