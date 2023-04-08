from google_play_scraper import app


def scrap_app(pkg: str):
    try:
        return app(pkg)
    except Exception as e:
        return False
