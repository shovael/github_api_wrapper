import argparse

from github_api_wrapper.wrapper_functions import latest_releases, forks_sum, stars_sum, contributors_sum, \
    pr_sum, contributors_ordered


def main():
    parser = argparse.ArgumentParser(
        prog='github_api_wrapper',
        description='wraps some of githubs api calls')
    parser.add_argument("-T", "--token", help="The github access token", required=True)
    parser.add_argument("-R", "--repo", help="The repo you want to query", required=True)
    parser.add_argument("-A", "--all-available-data", help="All th available data the wrapper has", action='store_true'
                        , dest='all')
    parser.add_argument("--latest-releases", help="The name of the last 3 releases", action='store_true')
    parser.add_argument("--forks-sum", help="The amount of forks project has", action='store_true')
    parser.add_argument("--stars-sum", help="The amount of stars the project has", action='store_true')
    parser.add_argument("--contributors-sum", help="The amount of contributors project has", action='store_true')
    parser.add_argument("--pr-sum", help="The amount of pr's project has", action='store_true')
    parser.add_argument("--contributors-ordered", help="A list of all the contributors ordered in a descending order "
                                                       "based on pr amount", action='store_true')

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
    if args.contributors_sum or args.all:
        result += contributors_sum(repo)
    if args.pr_sum or args.all:
        result += pr_sum(repo)
    if args.contributors_ordered or args.all:
        result += contributors_ordered(repo, token)
    print(result)


if __name__ == '__main__':
    main()
