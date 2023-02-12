from app import logger
from bs4 import BeautifulSoup


def parse_response(response):
    try:
        html_response = BeautifulSoup(response.text, 'html.parser')
        return html_response
    except Exception as e:
        logger.warning(e)
