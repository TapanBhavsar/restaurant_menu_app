from sqlalchemy import create_engine
import os

from database_lib.database_operations import DatabaseOperations

class SqlDatabaseOperations(DatabaseOperations):
    def __init__(self):
        super().__init__()
        self.database_folder = "sql_database"
        if not os.path.exists(self.database_folder):
            os.makedirs(self.database_folder)

    def create_database(self, database_name, table):
        database_path = self._get_database_path(database_name)
        if not os.path.exists(database_path):
            engine = create_engine('sqlite:///' + database_path)
            table.metadata.create_all(engine)
            return "database has been created."
        else:
            return "database is already created."

    def read_data(self, query):
        pass
    
    def update_data(self, query, data):
        pass

    def delete_data(self, query):
        pass

    def _get_database_path(self, database_name):
        if database_name.endswith(".db"):
            return os.path.join(self.database_folder,database_name)
        else:
            return os.path.join(self.database_folder,database_name) + ".db"
