from os import path, scandir
from typing import List


class OrgRepoMap:
    org: str
    repos: List[str]


def scan_for_orgs(data_path):
    for org_directory in scandir(data_path):
        if org_directory.is_dir():
            yield org_directory.name


def scan_for_repos(data_path, org):
    # org/repo/prs.json
    for repo_directory in scandir(path.join(data_path, org)):
        if repo_directory.is_dir():
            yield repo_directory.name


def scan_data(data_path):
    result = scan_for_orgs(data_path)
    for org in result:
        repos = scan_for_repos(data_path, org)
        print(org)
        for repo in repos:
            print(f'   > {repo}')


if __name__ == "__main__":
    data_path = './data/'
    scan_data(data_path)
