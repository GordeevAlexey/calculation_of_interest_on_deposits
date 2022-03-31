import sqlite3
from bd.utils import *

class DBContext:
    def __init__(self):
        self.conn = sqlite3.connect(PATH)
        self.cursor = self.conn.cursor()

    def get_contribution_name(self):
        result = []
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_NAME)
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
        return result

    def get_contribution_day(self, contribution_name):
        result = []
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_DAY, [contribution_name])
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
        return result

    def get_contribution_schema_bd(self, name, day):
        args = (name, day)
        result = []
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_SCHEMA, args)
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
        return result

    def get_contribution_percent(self, name, day, schema):
        args = (name, day, schema)
        result = []
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_PERCENT, args)
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
            result.append(n[1])
            result.append(n[2])
        return result

    def get_contribution_extra_option(self, name, key_options):
        args = (name, key_options)
        result = {}
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_EXTRA_OPTION_TXT, args)
        record = self.cursor.fetchall()
        text_message = record[0][0]
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_EXTRA_OPTION, args)
        record = self.cursor.fetchall()
        for n in record:
            result.update({n[0]: n[1]})
        return text_message, result

    def get_contribution_max_summ(self):
        result = []
        self.cursor.execute(SQL_QUERY_GET_MAX_SUM)
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
        return result

    def get_contribution_where_percent(self, contribution_name):
        result = []
        self.cursor.execute(SQL_QUERY_GET_CONTRIBUTION_WHERE_PERCENT, [contribution_name])
        record = self.cursor.fetchall()
        for n in record:
            result.append(n[0])
        return result