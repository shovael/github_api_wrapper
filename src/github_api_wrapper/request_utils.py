import requests


def _make_request_api(url: str, token: str) -> requests.Response:
    return requests.get(url=url, headers={'Authorization': 'Bearer {token}'.format(token=token),
                                          'X-GitHub-Api-Version': '2022-11-28'})


def _make_request_raw(url: str) -> requests.Response:
    return requests.get(url=url)

