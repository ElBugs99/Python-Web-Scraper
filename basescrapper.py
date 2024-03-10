import traceback
from abc import ABC, abstractmethod
from . import utils


class BaseScrapper(ABC):
    def __init__(self, filename, name):
        self.connection = utils.make_mongo_con().usa
        self.logger = utils.create_logger(filename, name)

    def start(self):
        start_url = self.get_initial_url()

        try:
            for data in self.create_next_url(start_url):
                try:
                    entity = self.get_item_data(data)
                    self.save(entity)
                except Exception as inner_ex:
                    print(traceback.format_exc())
                    self.logger.error(inner_ex)
        except Exception as ex:
            print(traceback.format_exc())
            self.logger.error(ex)

    @abstractmethod
    def get_initial_url(self):
        raise NotImplementedError('method get_initial_url is not implemented')

    @abstractmethod
    def create_next_url(self, start_url):
        raise NotImplementedError('method get_initial_url is not implemented')

    @abstractmethod
    def get_item_data(self, data):
        raise NotImplementedError('method get_item_data is not implemented')

    @abstractmethod
    def save(self, entity):
        raise NotImplementedError('method save is not implemented')
