from flask import Blueprint
api = Blueprint('api', __name__)


from . import user_route,products_route