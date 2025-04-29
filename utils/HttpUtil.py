import requests
from curl_cffi import requests as cffi_requests
import tls_client

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
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get(url):
    """
    Sends a GET request to the specified.

    :param url: The URL to send the GET request to.
    :param bearer_token: The Bearer token for authorization.
    :return: The response from the server.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_cffi(url):
    """
    使用curl_cffi發送 GET 請求到指定的 URL
    模擬TLS Fingerprinting
    """

    try:
        response = cffi_requests.get(url, impersonate="edge")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_tls_client(url):
    """
    使用tls_client發送 GET 請求到指定的 URL
    模擬TLS Fingerprinting
    需要打包tls-client-64.dll，在spec加入以下內容：
    datas=[('C:\\Users\\Max\\AppData\\Roaming\\Python\\Python312\\site-packages\\tls_client\\dependencies\\tls-client-64.dll', 'tls_client/dependencies')],
    """

    try:
        # 建立模擬 Chrome 的 session（會模擬 TLS 握手）
        session = tls_client.Session(
            client_identifier="chrome_120",  # 模擬 Chrome 120 的 TLS 設定
            random_tls_extension_order=True  # 更像真人操作
        )

        # 加上標準的瀏覽器 header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

        # 發送 GET 請求
        response = session.get(url, headers=headers)
        # 印出狀態碼與內容
        print("Status Code:", response.status_code)
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
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
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
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
        try:
            return response.json()
        except ValueError:
            # 如果不是 JSON 格式，就回傳原始文字
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None