import traceback
import requests
from abc import ABC, abstractmethod
from . import utils


class BaseApiScrapper(ABC):
    def __init__(self, filename, url, name):
        self.filename = filename
        self.connection = utils.make_mongo_con().usa
        self.logger = utils.create_logger(filename, name)
        self.response = self._fetch_data(url)

    def _fetch_data(self, url):
        return requests.get(url, verify=False).json()

    @abstractmethod
    def process_data(self):
        raise NotImplementedError('method process_data is not implemented')

    def start(self):
        try:
            data = self.process_data(self.response)
        except Exception as ex:
            print(traceback.format_exc())
            self.logger.error(ex)

    def save(self, data):
        try:
            self.connection[self.filename].insert_one(data.json)
        except TypeError:
            self.connection.errors.insert_one(data.to_dict(False))
