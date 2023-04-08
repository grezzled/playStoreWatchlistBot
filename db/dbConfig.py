import logging
import os.path
import sqlite3 as sql
from dotenv import load_dotenv

load_dotenv()
db_file = os.getenv('DB_FILE')


def _get_con():
    return sql.connect(db_file)


def _is_db_exist():
    return os.path.isfile(db_file)


def build_db():
    if _is_db_exist() is False:
        con = _get_con()
        print('building_db')
        with con:
            con.execute("""
            create table users (id integer not null primary key);
        """)
        with con:
            con.execute("""
                create table pkgs (pkg string not null primary key, user_id integer not null, foreign key(user_id) references users(id));
            """)


class dbConfig:
    con = None

    def __init__(self):
        if self.con is None:
            self.con = _get_con()

    def add_user(self, user_id: int):
        # TODO validate ID, make sure it is an integer
        sql_string = 'insert into users (id) values(?)'
        data = [user_id]
        with self.con:
            try:
                self.con.execute(sql_string, data)
            except NameError:
                pass

    def add_pkg(self, pkg: str, user_id: int):
        # TODO validate pkg, make sure it is an application pkg name
        sql_string = 'insert into pkgs (pkg, user_id) values(?,?)'
        data = [(pkg, user_id)]
        with self.con:
            self.con.executemany(sql_string, data)

    def del_pkg(self, pkg: str):
        sql_string = ' DELETE FROM pkgs WHERE pkg=(?)'
        data = [pkg]
        with self.con:
            self.con.execute(sql_string, data)

    def get_pkgs(self, user_id: int) -> []:
        sql_string = 'SELECT pkg FROM pkgs WHERE user_id <= (?)'
        data = [user_id]
        rows = []
        with self.con:
            cursor = self.con.execute(sql_string, data)
            for r in cursor:
                rows.append(r[0])
        return rows

    def get_pkg(self, pkg: str) -> []:
        sql_string = 'SELECT pkg FROM pkgs WHERE pkg = (?)'
        data = [pkg]
        rows = []
        with self.con:
            cursor = self.con.execute(sql_string, data)
            for r in cursor:
                rows.append(r[0])
        return rows
