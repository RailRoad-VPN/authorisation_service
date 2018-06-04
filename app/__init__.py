import logging
import os
from pprint import pprint

import sys
from flask import Flask, request

from api import register_api
from app.resources.user import UserAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load config based on env variable
ENVIRONMENT_CONFIG = os.environ.get("ENVIRONMENT_CONFIG", default='DevelopmentConfig')
logging.info("Got ENVIRONMENT_CONFIG variable: %s" % ENVIRONMENT_CONFIG)
config_name = "%s.%s" % ('config', ENVIRONMENT_CONFIG)
logging.info("Config name: %s" % config_name)
app.config.from_object(config_name)

app_config = app.config
api_base_uri = app_config['API_BASE_URI']

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

apis = [
    {'cls': UserAPI, 'args': [db_storage_service, app_config]},
]

register_api(app, api_base_uri, apis)

pprint(app.url_map._rules_by_endpoint)
