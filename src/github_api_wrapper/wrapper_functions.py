from typing import Any, List, Dict, Tuple
import re
import requests

from .request_utils import _make_request_api, _make_request_raw

GITHUB_API_URL: str = "https://api.github.com/"
GITHUB_URL: str = "https://github.com/"
REPOS_KEY: str = 'repos'


def _get_contributors(repo: str, url_extension: str, pr_user_pattern: str, name_extractor_pattern: str,
                      res_dict: Dict[str, int]) -> Dict[str, int]:
    running: bool = True
    counter: int = 1

    while running:
        url: str = GITHUB_URL + '{repo_name}'.format(repo_name=repo) + url_extension.format(page_num=counter)
        response: requests.Response = _make_request_raw(url)
        open_prs: List[str] = re.findall(pr_user_pattern, response.text)
        if not open_prs:
            running = False
        else:
            for res in open_prs:
                name: str = re.findall(name_extractor_pattern, res)[0]
                name = name.replace("\"", "")
                res_dict[name] = res_dict.setdefault(name, 0) + 1
            counter += 1
    return res_dict


def _get_contributors_details(repo: str, token: str, url_extension: str) -> List[Dict[str, Any]]:
    res = _make_request_api(url=GITHUB_API_URL + REPOS_KEY + "/" + repo + url_extension, token=token)
    full_res = res.json()
    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'],
                           headers={"Authorization": "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"})
        full_res.extend(res.json())
    return full_res


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
    url: str = GITHUB_URL + '{repo_name}'.format(repo_name=repo)
    response: requests.Response = _make_request_raw(url)
    res = re.findall(find_contributors_aria, response.text)[-1]
    regx_res = re.findall(extract_number, res)[-1]
    return result.format(regx_res)


def pr_sum(repo: str) -> str:
    open_pr_pattern: str = r'\S*\d+ Open'
    closed_pr_pattern: str = r'\S*\d+ Closed'
    url_extension: str = "/pulls?q=is%3Aclosed+is%3Aopen+is%3Apr"

    result: str = 'amount of pr\'s in this project is: {open} and {closed}\n'
    url: str = GITHUB_URL + '{repo_name}'.format(repo_name=repo) + url_extension
    response: requests.Response = _make_request_raw(url)
    open_pr: str = re.findall(open_pr_pattern, response.text)[-1]
    closed_pr: str = re.findall(closed_pr_pattern, response.text)[-1]
    return result.format(open=open_pr, closed=closed_pr)


def contributors_ordered(repo: str, token: str) -> str:
    open_pr_user_pattern: str = r"Open pull requests created by \S*"
    closed_pr_user_pattern: str = r"pull requests opened by \S*"
    name_extractor_pattern: str = r"(\S*)\"?$"
    url_extension_open: str = "/pulls?page={page_num}&q=is%3Aopen+is%3Apr"
    url_extension_closed: str = "/pulls?page={page_num}&q=is%3Apr+is%3Aclosed"
    url_extension_contributors_names: str = "/contributors?per_page=100"

    res_dict: Dict[str, int] = {}
    res_dict = _get_contributors(repo, url_extension_open, open_pr_user_pattern, name_extractor_pattern, res_dict)
    res_dict = _get_contributors(repo, url_extension_closed, closed_pr_user_pattern, name_extractor_pattern, res_dict)

    contributors_details: List[Dict[str, Any]] = _get_contributors_details(repo, token, url_extension_contributors_names)
    contributors_names: List[str] = [res['login'] for res in contributors_details]

    res_dict = {key: val for key, val in res_dict.items() if key in contributors_names}
    ordered_result: List[Tuple[str, int]] = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)
    result_str = '\n'.join(["{name}: {amount}".format(name=name, amount=amount) for name, amount in ordered_result])
    return result_str
