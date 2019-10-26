#!/usr/local/bin/python3

from github import Github

import json
import logging
from os import getenv, path

logging.basicConfig(level=logging.INFO)


"""UserPullRequest

    user
    title
    id (maybe for getting more info later?)
    created_at (datetime)
    closed_at (datetime)
    merged (bool)
    additions (int)
    deletions (int)

    .get_files()
      (file: filename, sha, previous_filename, additions, deletions, raw_url)
    .get_reviews()
      (pr review: user, submitted_at, url, commit_id, body, state)
"""


class UserPullRequest(object):
    def __init__(self, ghPR):
        self.number = ghPR.number
        self.user = ghPR.user.login
        self.title = ghPR.title
        self.created_at = str(ghPR.created_at)
        self.closed_at = str(ghPR.closed_at)
        self.githubID = ghPR.user.id
        self.merged = ghPR.merged
        self.additions = ghPR.additions
        self.deletions = ghPR.deletions
        self.filenames = []
        self.populate(ghPR)

    def populate(self, ghPR):
        files = ghPR.get_files()
        for f in files:
            self.filenames.append(str(f.filename))

    def to_dict(self):
        return {
            'number': self.number,
            'user': str(self.user),
            'title': str(self.title),
            'created_at': self.created_at,
            'closed_at': self.closed_at,
            'merged': self.merged,
            'additions': self.additions,
            'deletions': self.deletions,
            'filenames': self.filenames,
        }


def get_pull_requests(org: str, repo_name: str):
    data_dir = getenv('DATA_DIR')
    api_key = getenv('API_KEY')

    g = Github(api_key)
    logging.info('getting prs for %s/%s', org, repo_name)
    repo = g.get_repo(f'{org}/{repo_name}')
    pr = repo.get_pulls(
        sort='updated', direction='desc', base='master', state='closed')

    previous_prs = None
    previous_pr_titles = None 
    data_file = f'{data_dir}{org}/{repo_name}/prs.json'

    try:
        with open(data_file) as jsonfile:
            previous_prs = json.load(jsonfile)
            previous_pr_numbers = map(lambda x: x['number'], previous_prs['prs'])
    except FileNotFoundError:
        previous_pr_titles = [] 

    data = []
    try:
        for i, p in enumerate(pr):
            logging.debug('%s (%d) %d', p.title, p.number, i)
            if p.number in previous_pr_numbers:
                logging.info(
                    'Found matching PR title (%s) and number (%d), so breaking at %d.',
                    p.title, p.number, i)
                break
            logging.info('Processed %d PRs, current: %s (%d)', i, p.title, p.number)
            upr = UserPullRequest(p)
            data.append(upr.to_dict())
    except Exception:
        write_prs_to_files(data_file, data, True)
        exit(1)
    finally:
        write_prs_to_files(data_file, data, False)

def write_prs_to_files(filename: str, data: object, skip_if_empty: bool):
    if not path.exists(filename) and skip_if_empty:
        logging.info('not overwriting since file exists, %s', filename)
        return False

    if len(data) == 0:
        logging.info('no data to write, %s', filename)
        return False

    with open(filename,"w+") as f:
        logging.info('overwriting file, %s', filename)
        f.write(json.dumps({'prs': data}, indent=4))

    return True


if __name__ == '__main__':
    org = getenv('ORG_NAME')
    repo_name = getenv('REPO_NAME')
    get_pull_requests(org, repo_name)
