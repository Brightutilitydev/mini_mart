#!/usr/bin/env python3
"""Blueprints for the api"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/products")

from api.v1.views.products import *
