import logging
import os.path
import sqlite3 as sql
from dotenv import load_dotenv
from db.appModal import appModal
from datetime import datetime, date

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
            create table users (id integer not null primary key, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
        """)
        with con:
            con.execute("""
                create table pkgs (pkg string not null primary key, user_id integer not null, created_at DATETIME 
                DEFAULT CURRENT_TIMESTAMP, foreign key(user_id) references users(id));
            """)
        with con:
            con.execute("""create table apps (pkg string not null primary key, user_id integer not null, 
            title string, description string, descriptionHTML string, summary string, installs string, minInstalls 
            string, realInstalls string, score string, ratings string, reviews string, price string, free string, 
            currency string, sale string, saleTime string, originalPrice string, saleText string, offersIAP string, 
            inAppProductPrice string, developer string, developerId string, developerEmail string, developerWebsite 
            string, developerAddress string, privacyPolicy string, genre string, genreId string, icon string, 
            headerImage string, video string, videoImage string, contentRating string, contentRatingDescription 
            string, adSupported string, containsAds string, released string, updated string, version  string, 
            url string, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, foreign key(user_id) references users(id));""")
        with con:
            con.execute("""create table apps_logs (pkg string not null, user_id integer not null, 
            title string, description string, descriptionHTML string, summary string, installs string, minInstalls 
            string, realInstalls string, score string, ratings string, reviews string, price string, free string, 
            currency string, sale string, saleTime string, originalPrice string, saleText string, offersIAP string, 
            inAppProductPrice string, developer string, developerId string, developerEmail string, developerWebsite 
            string, developerAddress string, privacyPolicy string, genre string, genreId string, icon string, 
            headerImage string, video string, videoImage string, contentRating string, contentRatingDescription 
            string, adSupported string, containsAds string, released string, updated string, version  string, 
            url string, created_at DATETIME DEFAULT CURRENT_TIMESTAMP);""")


class dbConfig:
    con = None

    def __init__(self):
        if self.con is None:
            self.con = _get_con()

    def add_app(self, appModal: appModal):
        sql_string = """insert into apps(pkg, user_id, title, description, descriptionHTML, summary, installs, 
        minInstalls, realInstalls,score , ratings , reviews , price , free , currency , sale , saleTime , 
        originalPrice , saleText , offersIAP , inAppProductPrice , developer , developerId , developerEmail , 
        developerWebsite , developerAddress , privacyPolicy , genre , genreId , icon , headerImage , video , 
        videoImage , contentRating , contentRatingDescription , adSupported , containsAds , released , updated , 
        version  , url) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data = [(appModal.pkg, appModal.user_id, appModal.title, appModal.description, appModal.descriptionHTML,
                 appModal.summary, appModal.installs, appModal.minInstalls, appModal.realInstalls, appModal.score,
                 appModal.ratings,
                 appModal.reviews, appModal.price, appModal.free, appModal.currency, appModal.sale, appModal.saleTime,
                 appModal.originalPrice, appModal.saleText, appModal.offersIAP, appModal.inAppProductPrice,
                 appModal.developer, appModal.developerId, appModal.developerEmail, appModal.developerWebsite,
                 appModal.developerAddress, appModal.privacyPolicy, appModal.genre, appModal.genreId, appModal.icon,
                 appModal.headerImage, appModal.video, appModal.videoImage, appModal.contentRating,
                 appModal.contentRatingDescription, appModal.adSupported, appModal.containsAds, appModal.released,
                 appModal.updated, appModal.version, appModal.url
                 )]
        with self.con:
            try:
                self.con.executemany(sql_string, data)
            except Exception as x:
                print(x)

    def add_app_log(self, appModal: appModal):
        sql_string = """insert into apps_logs(pkg, user_id, title, description, descriptionHTML, summary, installs, 
        minInstalls, realInstalls,score , ratings , reviews , price , free , currency , sale , saleTime , 
        originalPrice , saleText , offersIAP , inAppProductPrice , developer , developerId , developerEmail , 
        developerWebsite , developerAddress , privacyPolicy , genre , genreId , icon , headerImage , video , 
        videoImage , contentRating , contentRatingDescription , adSupported , containsAds , released , updated , 
        version  , url) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data = [(appModal.pkg, appModal.user_id, appModal.title, appModal.description, appModal.descriptionHTML,
                 appModal.summary, appModal.installs, appModal.minInstalls, appModal.realInstalls, appModal.score,
                 appModal.ratings,
                 appModal.reviews, appModal.price, appModal.free, appModal.currency, appModal.sale, appModal.saleTime,
                 appModal.originalPrice, appModal.saleText, appModal.offersIAP, appModal.inAppProductPrice,
                 appModal.developer, appModal.developerId, appModal.developerEmail, appModal.developerWebsite,
                 appModal.developerAddress, appModal.privacyPolicy, appModal.genre, appModal.genreId, appModal.icon,
                 appModal.headerImage, appModal.video, appModal.videoImage, appModal.contentRating,
                 appModal.contentRatingDescription, appModal.adSupported, appModal.containsAds, appModal.released,
                 appModal.updated, appModal.version, appModal.url
                 )]
        with self.con:
            try:
                self.con.executemany(sql_string, data)
            except Exception as x:
                print(x)

    def get_app(self, pkg: str) -> []:
        sql_string = 'SELECT pkg FROM apps WHERE pkg = (?)'
        data = [pkg]
        rows = []
        with self.con:
            cursor = self.con.execute(sql_string, data)
            for r in cursor:
                rows.append(r[0])
        return rows

    def add_user(self, user_id: int):
        # TODO validate ID, make sure it is an integer
        sql_string = 'insert into users (id) values(?)'
        data = [user_id]
        with self.con:
            try:
                self.con.execute(sql_string, data)
            except Exception as e:
                print(str(e))

    def add_pkg(self, pkg: str, user_id: int):
        # TODO validate pkg, make sure it is an application pkg name
        sql_string = 'insert into pkgs (pkg, user_id) values(?,?)'
        data = [(pkg, user_id)]
        with self.con:
            try:
                self.con.executemany(sql_string, data)
            except Exception as e:
                print(str(e))

    def del_pkg(self, pkg: str):
        sql_string = ' DELETE FROM pkgs WHERE pkg=(?)'
        data = [pkg]
        with self.con:
            self.con.execute(sql_string, data)

    def get_pkgs(self, user_id: int) -> []:
        sql_string = 'SELECT pkg FROM pkgs WHERE user_id = (?)'
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

    def get_pkg_by_user_id(self, pkg: str, user_id: int) -> []:
        sql_string = 'SELECT pkg FROM pkgs WHERE pkg = (?) AND user_id = (?)'
        data = (pkg, user_id)
        rows = []
        with self.con:
            cursor = self.con.execute(sql_string, data)
            for r in cursor:
                rows.append(r[0])
        return rows
