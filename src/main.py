import argparse

from github_api_wrapper import latest_releases, forks_sum, stars_sum


def main():
    parser = argparse.ArgumentParser(
        prog='github_api_wrapper',
        description='wraps some of githubs api calls')
    parser.add_argument("-T", "--token", help="The github access token", required=True)
    parser.add_argument("-R", "--repo", help="The repo you want to query", required=True)
    parser.add_argument("-A", "--all-available-data", help="All th available data the wrapper has", action='store_true'
                        , dest='all')
    parser.add_argument("--latest-releases", help="The name of the last 3 releases", action='store_true')
    parser.add_argument("--forks-sum", help="The amount of forks", action='store_true')
    parser.add_argument("--stars-sum", help="The amount of stars the project has", action='store_true')

    args = parser.parse_args()

    result: str = ''
    token: str = args.token
    repo: str = args.repo
    if args.latest_releases or args.all:
        result += latest_releases(token, repo)
    if args.forks_sum or args.all:
        result += forks_sum(token, repo)
    if args.stars_sum or args.all:
        result += stars_sum(token, repo)
    print(result)

    # import requests
    # res = requests.get(url="https://api.github.com/repos/CTFd/CTFd/stargazers",
    #                    headers={'Authorization': 'Bearer {token}'.format(token=token)}).json()
    # print(res['stargazers_count'], res['stargazers_url'])
    # print(res[29])

if __name__ == '__main__':
    main()
