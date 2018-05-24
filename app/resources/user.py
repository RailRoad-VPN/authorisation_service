import json
import logging
import sys
from http import HTTPStatus

from flask import Response, request

from app.exception import AuthError, UserException, UserNotFoundException
from app.model.user import UserDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import JSONDecimalEncoder, check_uuid, make_api_response
from api import ResourceAPI
from response import APIResponseStatus, APIResponse


class UserAPI(ResourceAPI):
    __version__ = 1

    __api_url__ = 'users'

    _config = None

    __db_storage_service = None

    def __init__(self, db_storage_service: DBStorageService, config: dict) -> None:
        super().__init__()
        self._config = config
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        email = request_json.get(UserDB._email_field, None)
        created_date = request_json.get(UserDB._created_date_field, None)
        password = request_json.get(UserDB._password_field, None)
        is_expired = request_json.get(UserDB._is_expired_field, None)
        is_locked = request_json.get(UserDB._is_locked_field, None)
        is_password_expired = request_json.get(UserDB._is_password_expired_field, None)
        enabled = request_json.get(UserDB._enabled_field, None)

        user_db = UserDB(storage_service=self.__db_storage_service, email=email,
                         is_password_expired=is_password_expired, password=password, created_date=created_date,
                         is_expired=is_expired, is_locked=is_locked, enabled=enabled)

        try:
            suuid = user_db.create()
        except UserException as e:
            logging.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            if error_code == AuthError.USER_CREATE_ERROR_DB:
                http_code = HTTPStatus.BAD_REQUEST
            else:
                http_code = HTTPStatus.INTERNAL_SERVER_ERROR
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(json.dumps(response_data.serialize()), http_code)

        resp = make_api_response('', HTTPStatus.CREATED)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def put(self, suuid: str = None) -> Response:
        request_json = request.json

        user_uuid = request_json.get(UserDB._suuid_field, None)

        is_valid = check_uuid(suuid=user_uuid)
        is_valid_b = check_uuid(suuid=suuid)
        if not is_valid or not is_valid_b or suuid != user_uuid:
            error = AuthError.USER_FINDBYUUID_ERROR.phrase
            error_code = AuthError.USER_FINDBYUUID_ERROR
            developer_message = AuthError.USER_FINDBYUUID_ERROR.description
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        email = request_json.get(UserDB._email_field, None)
        password = request_json.get(UserDB._password_field, None)
        is_expired = request_json.get(UserDB._is_expired_field, None)
        is_locked = request_json.get(UserDB._is_locked_field, None)
        is_password_expired = request_json.get(UserDB._is_password_expired_field, None)
        enabled = request_json.get(UserDB._enabled_field, None)

        user_db = UserDB(storage_service=self.__db_storage_service, suuid=user_uuid, email=email,
                         is_password_expired=is_password_expired, password=password, is_expired=is_expired,
                         is_locked=is_locked, enabled=enabled)

        try:
            user_db.update()
        except UserException as e:
            logging.error(e)
            http_code = HTTPStatus.BAD_REQUEST
            error = e.error
            error_code = e.error_code
            developer_message = e.developer_message
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp

        resp = make_api_response('', HTTPStatus.NO_CONTENT)
        resp.headers['Location'] = '%s/%s/uuid/%s' % (self._config['API_BASE_URI'], self.__api_url__, suuid)
        return resp

    def get(self, suuid: str = None, email: str = None) -> Response:
        super(UserAPI, self).get(req=request)
        if suuid is not None:
            is_valid = check_uuid(suuid=suuid)
            if not is_valid:
                error = AuthError.USER_FINDBYUUID_ERROR.phrase
                error_code = AuthError.USER_FINDBYUUID_ERROR
                developer_message = AuthError.USER_FINDBYUUID_ERROR.description
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
        user_db = UserDB(storage_service=self.__db_storage_service, suuid=suuid, email=email,
                         limit=self.pagination.limit, offset=self.pagination.offset)
        if suuid is None and email is None:
            # find all user is no parameter set
            try:
                user_list = user_db.find_all()
                users_dict = [user_list[i].to_dict() for i in range(0, len(user_list))]
                response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK, data=users_dict)
                resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
                return resp
            except UserException as e:
                logging.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
        elif suuid is not None:
            # find user by suuid
            try:
                user = user_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                            data=user.to_dict())
                resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
                return resp
            except UserNotFoundException as e:
                logging.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
            except UserException as e:
                logging.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
        elif email is not None:
            # find user by email
            try:
                user = user_db.find_by_email()
                response_data = APIResponse(status=APIResponseStatus.success.value, code=HTTPStatus.OK,
                                            data=user.to_dict())
                resp = make_api_response(json.dumps(response_data.serialize(), cls=JSONDecimalEncoder), HTTPStatus.OK)
                return resp
            except UserNotFoundException as e:
                logging.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
            except UserException as e:
                logging.error(e)
                http_code = HTTPStatus.INTERNAL_SERVER_ERROR
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(json.dumps(response_data.serialize()), http_code)
                return resp
        else:
            http_code = HTTPStatus.SERVICE_UNAVAILABLE
            error = AuthError.UNKNOWN_ERROR_CODE.phrase
            error_code = AuthError.UNKNOWN_ERROR_CODE
            response_data = APIResponse(status=APIResponseStatus.failed.value, code=http_code, error=error,
                                        error_code=error_code)
            resp = make_api_response(json.dumps(response_data.serialize()), http_code)
            return resp
