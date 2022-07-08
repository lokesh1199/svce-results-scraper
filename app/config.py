import os


def getSecretKey():
    return os.getenv('SCRAPER_SECRET_KEY')
