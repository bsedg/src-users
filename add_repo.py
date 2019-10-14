from errno import EEXIST
import logging
from os import mkdir, path


def create_repo(data_path, org_name, repo_name):
    create_dir(path.join(data_path, org_name))
    create_dir(path.join(data_path, org_name, repo_name))


def create_dir(path):
    try:
        mkdir(path)
    except OSError as exc:
        if exc.errno != EEXIST:
            logging.debug('path already exists: %s', path)
        pass


if __name__ == '__main__':
    create_repo('./data/', 'bsedg', 'events-api')
