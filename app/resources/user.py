import json
import logging
import sys
import uuid as uuidlib

from flask import Response, request, make_response

from app.exception import AuthError, UserException, UserNotFoundException
from app.model.user import UserDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from decoder import JSONDecimalEncoder
from api import ResourceAPI


class UserAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'users'

    _config = None

    __uuid_field = 'uuid'
    __email_field = 'email'
    __password_field = 'password'
    __account_non_expired_field = 'account_non_expired'
    __account_non_locked_field = 'account_non_locked'
    __credentials_non_expired_field = 'credentials_non_expired'
    __enabled_field = 'enabled'

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        email = request_json[self.__email_field]
        password = request_json.get(self.__password_field, None)
        account_non_expired = request_json.get(self.__account_non_expired_field, True)
        account_non_locked = request_json.get(self.__account_non_locked_field, True)
        credentials_non_expired = request_json.get(self.__credentials_non_expired_field, True)
        enabled = request_json.get(self.__enabled_field, True)

        user_db = UserDB(storage_service=self.__db_storage_service, email=email,
                         password=password, account_non_expired=account_non_expired,
                         account_non_locked=account_non_locked, credentials_non_expired=credentials_non_expired,
                         enabled=enabled)

        try:
            uuid = user_db.create()
        except UserException as e:
            logging.error(e)
            code = e.code
            message = e.message
            data_err = e.data
            data = {
                'error': {
                    'code': code,
                    'message': message,
                    'data': data_err
                }
            }
            if code == AuthError.USER_CREATE_ERROR_DB:
                http_code = 400
            else:
                http_code = 500
            return make_response(json.dumps(data), http_code)

        resp = make_response("", 201)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def put(self, uuid: str = None) -> Response:
        request_json = request.json
        user_uuid = request_json[self.__uuid_field]
        if uuid != user_uuid:
            return make_response('', 404)

        try:
            uuidlib.UUID(user_uuid)
        except ValueError as e:
            message = 'User not found'
            developer_message = 'Bad uuid value.'
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            logging.error(e)
            data_err = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            data = {
                'error': {
                    'code': system_error_code,
                    'message': message,
                    'data': data_err
                }
            }
            resp = make_response(json.dumps(data), 404)
            return resp

        email = request_json[self.__email_field]
        password = request_json[self.__password_field]
        account_non_expired = request_json[self.__account_non_expired_field]
        account_non_locked = request_json[self.__account_non_locked_field]
        credentials_non_expired = request_json[self.__credentials_non_expired_field]
        enabled = request_json[self.__enabled_field]

        user_db = UserDB(storage_service=self.__db_storage_service, uuid=user_uuid, email=email,
                         password=password, account_non_expired=account_non_expired,
                         account_non_locked=account_non_locked, credentials_non_expired=credentials_non_expired,
                         enabled=enabled)
        user_db.update()

        resp = make_response("", 200)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (self._config['API_BASE_URI'], self.__api_url__, uuid)
        return resp

    def get(self, uuid: str = None, email: str = None) -> Response:
        if uuid is not None:
            try:
                uuidlib.UUID(uuid)
            except ValueError as e:
                message = 'User not found'
                developer_message = 'Bad uuid value.'
                system_error_code = AuthError.USER_FINDBYUUID_ERROR
                logging.error(e)
                data_err = {
                    'system_error_code': system_error_code,
                    'developer_message': developer_message
                }
                data = {
                    'error': {
                        'code': system_error_code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
                return resp
        user_db = UserDB(storage_service=self.__db_storage_service, uuid=uuid, email=email)
        if uuid is None and email is None:
            # find all user is no parameter set
            try:
                user_list = user_db.find_all()
                resp = make_response(json.dumps([ob.to_dict() for ob in user_list], cls=JSONDecimalEncoder), 200)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            return resp
        elif uuid is not None:
            # find user by uuid
            try:
                user = user_db.find_by_uuid()
                resp = make_response(json.dumps(user.to_dict(), cls=JSONDecimalEncoder), 200)
            except UserNotFoundException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 500)
        elif email is not None:
            # find user by email
            try:
                user = user_db.find_by_email()
                resp = make_response(json.dumps(user.to_dict(), cls=JSONDecimalEncoder), 200)
            except UserNotFoundException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 404)
            except UserException as e:
                logging.error(e)
                code = e.code
                message = e.message
                data_err = e.data
                data = {
                    'error': {
                        'code': code,
                        'message': message,
                        'data': data_err
                    }
                }
                resp = make_response(json.dumps(data), 500)
        else:
            data = {
                'error': {
                    'code': AuthError.UNKNOWN_ERROR_CODE,
                    'message': "UserAPI get method all parameters are null. WTF?"
                }
            }
            resp = make_response(json.dumps(data), 500)
        return resp
