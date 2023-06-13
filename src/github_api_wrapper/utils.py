from typing import Any, List, Dict
import re

import requests

GITHUB_API_URL: str = "https://api.github.com/"
GITHUB_URL: str = "https://github.com/"
REPOS_KEY: str = 'repos'


def _make_request_api(url: str, token: str) -> requests.Response:
    return requests.get(url=url, headers={'Authorization': 'Bearer {token}'.format(token=token),
                                          'X-GitHub-Api-Version': '2022-11-28'})


def _make_request_raw(url: str) -> requests.Response:
    return requests.get(url=url)


def latest_releases(token: str, repo: str) -> str:
    release_amount: int = 3

    result: str = 'last {} releases are:\n'.format(release_amount)
    url: str = GITHUB_API_URL + REPOS_KEY + '/{repo_name}/releases'.format(repo_name=repo)
    response: requests.Response = _make_request_api(url, token)
    response_json: List[Dict[str: Any]] = response.json()
    for i in range(1, release_amount + 1):
        result += '{number}: {release_name}\n'.format(number=i, release_name=response_json[i]['name'])
    return result


def forks_sum(token: str, repo: str) -> str:
    result: str = 'total numbers of forks is: {}\n'
    url: str = GITHUB_API_URL + REPOS_KEY + '/{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request_api(url, token)
    return result.format(response.json()['forks'])


def stars_sum(token: str, repo: str) -> str:
    result: str = 'amount of starts the project has: {}\n'
    url: str = GITHUB_API_URL + REPOS_KEY + '/{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request_api(url, token)
    return result.format(response.json()['stargazers_count'])


def contributors_sum(repo: str) -> str:
    find_contributors_aria: str = r'Contributors\n.*\d'
    extract_number: str = r'\d+'

    result: str = 'amount of contributors the project has: {}\n'
    url: str = GITHUB_URL + '/{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request_raw(url)
    res = re.findall(find_contributors_aria, response.text)[-1]
    regx_res = re.findall(extract_number, res)[-1]
    return result.format(regx_res)


def pr_sum(repo: str) -> str:
    open_pr_pattern: str = r'\S*\d+ Open'
    closed_pr_pattern: str = r'\S*\d+ Closed'
    url_extension: str = "/pulls?q=is%3Aclosed+is%3Aopen+is%3Apr"

    result: str = 'amount of pr\'s in this project is: {open} and {closed}\n'
    url: str = GITHUB_URL + '/{repo_name}'.format(repo_name=repo) + url_extension
    response: requests.Response = _make_request_raw(url)
    open_pr: str = re.findall(open_pr_pattern, response.text)[-1]
    closed_pr: str = re.findall(closed_pr_pattern, response.text)[-1]
    return result.format(open=open_pr, closed=closed_pr)
