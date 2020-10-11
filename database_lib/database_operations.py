import abc

class DatabaseOperations(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def create_database(self, database_name, table):
        pass

    @abc.abstractmethod
    def read_data(self, query):
        pass
    
    @abc.abstractmethod
    def update_data(self, query, data):
        pass

    @abc.abstractmethod
    def delete_data(self, query):
        pass