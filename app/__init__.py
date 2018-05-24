import logging
from pprint import pprint

import sys
from flask import Flask

from app.resources.user import UserAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.TestingConfig')

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

# USER API
user_api_url = '%s/%s' % (app.config['API_BASE_URI'], UserAPI.__api_url__)
user_api_view_func = UserAPI.as_view('user_api', db_storage_service, app.config)
app.add_url_rule(user_api_url, view_func=user_api_view_func, methods=['GET', 'POST'])
app.add_url_rule('%s/<string:suuid>' % user_api_url, view_func=user_api_view_func, methods=['PUT'])
app.add_url_rule('%s/uuid/<string:suuid>' % user_api_url, view_func=user_api_view_func, methods=['GET'])
app.add_url_rule('%s/email/<string:email>' % user_api_url, view_func=user_api_view_func, methods=['GET'])

pprint(app.url_map._rules_by_endpoint)
