import logging
import os
import sys
from http import HTTPStatus
from pprint import pprint

from flask import Flask, request

from app.exception import AuthError
from app.resources.users import UsersAPI
from app.resources.users.devices import UsersDevicesAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from response import make_error_request_response
from api import register_api

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load config based on env variable
ENVIRONMENT_CONFIG = os.environ.get("ENVIRONMENT_CONFIG", default='DevelopmentConfig')
logger.info("Got ENVIRONMENT_CONFIG variable: %s" % ENVIRONMENT_CONFIG)
config_name = "%s.%s" % ('config', ENVIRONMENT_CONFIG)
logger.info("Config name: %s" % config_name)
app.config.from_object(config_name)

app_config = app.config
api_base_uri = app_config['API_BASE_URI']

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

apis = [
    {'cls': UsersAPI, 'args': [db_storage_service, app_config]},
    {'cls': UsersDevicesAPI, 'args': [db_storage_service, app_config]},
]

register_api(app, api_base_uri, apis)


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


@app.errorhandler(400)
def not_found_error(error):
    return make_error_request_response(HTTPStatus.BAD_REQUEST)


@app.errorhandler(404)
def not_found_error(error):
    return make_error_request_response(HTTPStatus.NOT_FOUND)


@app.errorhandler(500)
def internal_error(error):
    return make_error_request_response(HTTPStatus.INTERNAL_SERVER_ERROR)


pprint(app.url_map._rules_by_endpoint)
