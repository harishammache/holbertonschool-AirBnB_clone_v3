from api.v1.views import states, cities, amenities, users
from api.v1.views import places, places_reviews
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
