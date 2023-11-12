# my_routes.py
from flask import Blueprint
from ..controllers.model_recommendation_controller import model_recommendation_controller

routes = Blueprint('routes', __name__)

# Daftarkan blueprint yang telah Anda buat
routes.register_blueprint(model_recommendation_controller)
