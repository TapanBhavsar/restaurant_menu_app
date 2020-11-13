from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jinja2 import Template

import os

from database_lib.database_operations import DatabaseOperations

class SqlDatabaseOperations(DatabaseOperations):
    def __init__(self):
        super().__init__()
        self.database_folder = "sql_database"
        if not os.path.exists(self.database_folder):
            os.makedirs(self.database_folder)

        self.QUERY_TEMPLATE_ONE = "self._session.query(table).filter_by({{ filter }}).one()"
        self.QUERY_TEMPLATE = "self._session.query(table).filter_by({{ filter }})"
        
        self._engine = None
        self._session = None

    def create_database(self, database_name, table):
        database_path = self._get_database_path(database_name)
        self._engine = create_engine('sqlite:///' + database_path)
        self._set_session()
        if not os.path.exists(database_path):
            table.metadata.create_all(self._engine)
            return "database has been created."
        else:
            return "database is already created."

    def add_data(self, data):
        self._session.add(data)
        try:
            self._session.commit()
        except:
            self._session.rollback()

    def read_data(self, table, filter, one=False):
        if one:
            query_template = Template(self.QUERY_TEMPLATE_ONE)
            return eval(query_template.render(table=table, filter=filter))
        else:
            query_template = Template(self.QUERY_TEMPLATE)
            return eval(query_template.render(table=table, filter=filter))

    def update_data(self, query, data):
        pass

    def delete_data(self, query):
        pass

    def _get_database_path(self, database_name):
        if database_name.endswith(".db"):
            return os.path.join(self.database_folder,database_name)
        else:
            return os.path.join(self.database_folder,database_name) + ".db"

    def _set_session(self):
        DBSession = sessionmaker(bind = self._engine)
        self._session = DBSession()