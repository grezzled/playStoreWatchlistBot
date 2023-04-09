class appModal:

    def __init__(self):
        self._pkg = ""
        self._user_id = ""
        self._title = ""
        self._description = ""
        self._descriptionHTML = ""
        self._summary = ""
        self._installs = ""
        self._minInstalls = ""
        self._realInstalls = ""
        self._score = ""
        self._ratings = ""
        self._reviews = ""
        self._price = ""
        self._free = ""
        self._currency = ""
        self._sale = ""
        self._saleTime = ""
        self._originalPrice = ""
        self._saleText = ""
        self._offersIAP = ""
        self._inAppProductPrice = ""
        self._developer = ""
        self._developerId = ""
        self._developerEmail = ""
        self._developerWebsite = ""
        self._developerAddress = ""
        self._privacyPolicy = ""
        self._genre = ""
        self._genreId = ""
        self._icon = ""
        self._headerImage = ""
        self._video = ""
        self._videoImage = ""
        self._contentRating = ""
        self._contentRatingDescription = ""
        self._adSupported = ""
        self._containsAds = ""
        self._released = ""
        self._updated = ""
        self._version = ""
        self._url = ""

    @property
    def genreId(self):
        return self._genreId

    @genreId.setter
    def genreId(self, genreId):
        self._genreId = genreId

    @property
    def contentRatingDescription(self):
        return self._contentRatingDescription

    @contentRatingDescription.setter
    def contentRatingDescription(self, contentRatingDescription):
        self._contentRatingDescription = contentRatingDescription

    @property
    def privacyPolicy(self):
        return self._privacyPolicy

    @privacyPolicy.setter
    def privacyPolicy(self, privacyPolicy):
        self._privacyPolicy = privacyPolicy

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @property
    def video(self):
        return self._video

    @video.setter
    def video(self, video):
        self._video = video

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def adSupported(self):
        return self._adSupported

    @adSupported.setter
    def adSupported(self, adSupported):
        self._adSupported = adSupported

    @property
    def containsAds(self):
        return self._containsAds

    @containsAds.setter
    def containsAds(self, containsAds):
        self._containsAds = containsAds

    @property
    def headerImage(self):
        return self._headerImage

    @headerImage.setter
    def headerImage(self, headerImage):
        self._headerImage = headerImage

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        self._genre = genre

    @property
    def videoImage(self):
        return self._videoImage

    @videoImage.setter
    def videoImage(self, videoImage):
        self._videoImage = videoImage

    @property
    def contentRating(self):
        return self._contentRating

    @contentRating.setter
    def contentRating(self, contentRating):
        self._contentRating = contentRating

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, updated):
        self._updated = updated

    @property
    def released(self):
        return self._released

    @released.setter
    def released(self, released):
        self._released = released

    @property
    def developerAddress(self):
        return self._developerAddress

    @developerAddress.setter
    def developerAddress(self, developerAddress):
        self._developerAddress = developerAddress

    @property
    def saleText(self):
        return self._saleText

    @saleText.setter
    def saleText(self, saleText):
        self._saleText = saleText

    @property
    def sale(self):
        return self._sale

    @sale.setter
    def sale(self, sale):
        self._sale = sale

    @property
    def saleTime(self):
        return self._saleTime

    @saleTime.setter
    def saleTime(self, saleTime):
        self._saleTime = saleTime

    @property
    def developerId(self):
        return self._developerId

    @developerId.setter
    def developerId(self, developerId):
        self._developerId = developerId

    @property
    def originalPrice(self):
        return self._originalPrice

    @originalPrice.setter
    def originalPrice(self, originalPrice):
        self._originalPrice = originalPrice

    @property
    def offersIAP(self):
        return self._offersIAP

    @offersIAP.setter
    def offersIAP(self, offersIAP):
        self._offersIAP = offersIAP

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, currency):
        self._currency = currency

    @property
    def developer(self):
        return self._developer

    @developer.setter
    def developer(self, developer):
        self._developer = developer

    @property
    def developerEmail(self):
        return self._developerEmail

    @developerEmail.setter
    def developerEmail(self, developerEmail):
        self._developerEmail = developerEmail

    @property
    def inAppProductPrice(self):
        return self._inAppProductPrice

    @inAppProductPrice.setter
    def inAppProductPrice(self, inAppProductPrice):
        self._inAppProductPrice = inAppProductPrice

    @property
    def developerWebsite(self):
        return self._developerWebsite

    @developerWebsite.setter
    def developerWebsite(self, developerWebsite):
        self._developerWebsite = developerWebsite

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        self._summary = summary

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def pkg(self):
        return self._pkg

    @pkg.setter
    def pkg(self, pkg):
        self._pkg = pkg

    @property
    def installs(self):
        return self._installs

    @installs.setter
    def installs(self, installs):
        self._installs = installs

    @property
    def realInstalls(self):
        return self._realInstalls

    @realInstalls.setter
    def realInstalls(self, realInstalls):
        self._realInstalls = realInstalls

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def minInstalls(self):
        return self._minInstalls

    @minInstalls.setter
    def minInstalls(self, minInstalls):
        self._minInstalls = minInstalls

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, reviews):
        self._reviews = reviews

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def ratings(self):
        return self._ratings

    @ratings.setter
    def ratings(self, ratings):
        self._ratings = ratings

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def descriptionHTML(self):
        return self._descriptionHTML

    @descriptionHTML.setter
    def descriptionHTML(self, descriptionHTML):
        self._descriptionHTML = descriptionHTML

    @property
    def free(self):
        return self._free

    @free.setter
    def free(self, free):
        self._free = free
