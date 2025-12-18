"""
Newsletter Blueprint
"""
from flask import Blueprint

newsletter_bp = Blueprint('newsletter', __name__)

from . import routes
