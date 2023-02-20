import logging

from mitmproxy import http

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class MyAddon:
    def __init__(self):
        pass
    
    def request(self, flow: http.HTTPFlow) -> None:
        logging.info(f'url: {flow.request.url}')

    def response(self, flow: http.HTTPFlow) -> None:
        pass


addons = [MyAddon()]
