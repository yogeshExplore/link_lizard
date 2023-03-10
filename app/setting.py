import os
import pathlib
import validators
import argparse

# todo testing
# todo flake 8


# todo should not be here
class ValidateUrl(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        url = values.strip('/').replace('www.', '').replace('https', 'http')
        if not validators.url(url):
            raise argparse.ArgumentError(self, 'Invalid Url format, url should be like "http://example.com"')
        setattr(namespace, self.dest, url)


def read_args():
    parser = argparse.ArgumentParser(description='Parameters for crawler')
    parser.add_argument('--type', dest='CRAWLER_TYPE',
                        action='store', required=False, help='website_links', type=str, default='website_links')
    parser.add_argument('--url', dest='BASE_URL',
                        action=ValidateUrl, required=False, type=str, default='http://example.com')
    parser.add_argument('--workers', dest='WORKERS', action='store',
                        required=False, type=int, help='number of workers', default=1)
    parser.add_argument('--output', dest='OUTPUT', action='store',
                        required=False, type=str, help='file|mongodb', default='file')
    return parser.parse_args()


class Setting:
    INPUT_ARGS = read_args()
    PROJECT_BASE_DIR = str(pathlib.Path(os.path.abspath(os.path.join(os.getcwd(), __file__))).parent.parent)
    OUTPUT_DIR = str(os.path.join(PROJECT_BASE_DIR, 'output'))  # cross-platform
    ALLOWED_ENVIRONMENT = {'STAGING', 'PRODUCTION'}

    ORGANISATION = 'Two'

    # Input Arguments
    CRAWLER_TYPE = INPUT_ARGS.CRAWLER_TYPE
    BASE_URL = INPUT_ARGS.BASE_URL
    WORKERS = INPUT_ARGS.WORKERS
    OUTPUT = INPUT_ARGS.OUTPUT

    FILE_PREFIX = 'website_crawler'
    BATCH_SIZE_DB_WRITE = 1000
