from flask import Blueprint

report = Blueprint('report', __name__)

from app.report import views
