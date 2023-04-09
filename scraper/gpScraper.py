import json

from google_play_scraper import app
from db.appModal import appModal
from db.dbConfig import dbConfig


def scrap_app(pkg: str, user_id):
    try:
        result = app(pkg)
        if result:
            a = get_app_modal(result, pkg, user_id)
            print(a)
            dbConfig().add_app(a)
    except Exception as e:
        print(str(e))
        return False


def get_app_modal(jsonData, pkg, user_id):
    r = json.loads(json.dumps(jsonData))
    a = appModal()
    a.pkg = pkg
    a.user_id = user_id
    a.title = r['title']
    a.description = r['description']
    a.descriptionHTML = r['descriptionHTML']
    a.summary = r['summary']
    a.installs = r['installs']
    a.minInstalls = r['minInstalls']
    a.realInstalls = r['realInstalls']
    a.score = r['score']
    a.ratings = r['ratings']
    a.reviews = r['reviews']
    a.price = r['price']
    a.free = r['free']
    a.currency = r['currency']
    a.sale = r['sale']
    a.saleTime = r['saleTime']
    a.originalPrice = r['originalPrice']
    a.offersIAP = r['offersIAP']
    a.inAppProductPrice = r['inAppProductPrice']
    a.developer = r['developer']
    a.developerId = r['developerId']
    a.developerEmail = r['developerEmail']
    a.developerWebsite = r['developerWebsite']
    a.developerAddress = r['developerAddress']
    a.privacyPolicy = r['privacyPolicy']
    a.genre = r['genre']
    a.genreId = r['genreId']
    a.icon = r['icon']
    a.headerImage = r['headerImage']
    a.video = r['video']
    a.videoImage = r['videoImage']
    a.contentRating = r['contentRating']
    a.contentRatingDescription = r['contentRatingDescription']
    a.adSupported = r['adSupported']
    a.containsAds = r['containsAds']
    a.released = r['released']
    a.updated = r['updated']
    a.version = r['version']
    a.url = r['url']
    return a
