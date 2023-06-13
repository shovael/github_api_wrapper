from typing import Any, List, Dict, Tuple

import requests

GITHUB_URL: str = "https://api.github.com/"
REPOS_KEY: str = 'repos'


def _make_request(url: str, token: str) -> requests.Response:
    return requests.get(url=url, headers={'Authorization': 'Bearer {token}'.format(token=token)})


def latest_releases(token: str, repo: str) -> str:
    release_amount: int = 3

    result: str = '\nlast {} releases are:\n'.format(release_amount)
    url: str = GITHUB_URL + REPOS_KEY + '/{repo_name}/releases'.format(repo_name=repo)
    response: requests.Response = _make_request(url, token)
    response_json: List[Dict[str: Any]] = response.json()
    for i in range(1, release_amount + 1):
        result += '{number}: {release_name}\n'.format(number=i, release_name=response_json[i]['name'])
    return result


def forks_sum(token: str, repo: str) -> str:
    result: str = '\ntotal numbers of forks is: {}\n'
    url: str = GITHUB_URL + REPOS_KEY + '/{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request(url, token)
    return result.format(response.json()['forks'])


def stars_sum(token: str, repo: str) -> str:
    result: str = '\namount of starts the project has: {}\n'
    url: str = GITHUB_URL + REPOS_KEY + '/{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request(url, token)
    return result.format(response.json()['stargazers_count'])
