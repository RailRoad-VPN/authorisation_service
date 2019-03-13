import logging
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import AuthError, UserException, UserNotFoundException
from app.model.user import UserDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI, APIResourceURL
from response import APIResponseStatus, APIResponse


class UsersAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'users'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = f"{base_url}/{UsersAPI.__api_url__}"
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['PUT']),
            APIResourceURL(base_url=url, resource_name='uuid/<string:suuid>', methods=['GET']),
            APIResourceURL(base_url=url, resource_name='email/<string:email>', methods=['GET']),
            APIResourceURL(base_url=url, resource_name='pincode/<string:pin_code>', methods=['GET']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.REQUEST_NO_JSON)

        email = request_json.get(UserDB._email_field, None)
        password = request_json.get(UserDB._password_field, None)
        is_expired = request_json.get(UserDB._is_expired_field, False)
        is_locked = request_json.get(UserDB._is_locked_field, False)
        is_password_expired = request_json.get(UserDB._is_password_expired_field, False)
        enabled = request_json.get(UserDB._enabled_field, True)

        req_fields = {
            'email': email,
            'password': password
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_db = UserDB(storage_service=self.__db_storage_service, email=email,
                         is_password_expired=is_password_expired, password=password,
                         is_expired=is_expired, is_locked=is_locked, enabled=enabled)

        try:
            user_db.find_by_email()
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.USER_CREATE_EMAIL_EXIST_ERROR)
        except UserNotFoundException:
            try:
                suuid = user_db.create()
            except UserException as e:
                self.logger.error(e)
                error_code = e.error_code
                error = e.error
                developer_message = e.developer_message
                http_code = HTTPStatus.BAD_REQUEST
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                return make_api_response(data=response_data, http_code=http_code)

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.CREATED)
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{self.__api_url__}/uuid/{suuid}"
        return resp

    def put(self, suuid: str = None) -> Response:
        request_json = request.json

        user_uuid = request_json.get(UserDB._suuid_field, None)

        is_valid = check_uuid(suuid=user_uuid)
        is_valid_b = check_uuid(suuid=suuid)
        if not is_valid or not is_valid_b or suuid != user_uuid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.USER_FINDBYUUID_ERROR)

        email = request_json.get(UserDB._email_field, None)
        password = request_json.get(UserDB._password_field, None)
        is_expired = request_json.get(UserDB._is_expired_field, None)
        is_locked = request_json.get(UserDB._is_locked_field, None)
        is_password_expired = request_json.get(UserDB._is_password_expired_field, None)
        enabled = request_json.get(UserDB._enabled_field, None)
        pin_code = request_json.get(UserDB._pin_code_field, None)
        pin_code_expire_date = request_json.get(UserDB._pin_code_expire_date_field, None)
        modify_reason = request_json.get(UserDB._modify_reason_field, None)
        is_pin_code_activated = request_json.get(UserDB._is_pin_code_activated_field, None)

        req_fields = {
            'email': email,
            'is_expired': is_expired,
            'is_locked': is_locked,
            'is_password_expired': is_password_expired,
            'enabled': enabled,
            'modify_reason': modify_reason,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_db = UserDB(storage_service=self.__db_storage_service, suuid=user_uuid, email=email,
                         is_password_expired=is_password_expired, password=password, is_expired=is_expired,
                         is_locked=is_locked, enabled=enabled, modify_reason=modify_reason, pin_code=pin_code,
                         pin_code_expire_date=pin_code_expire_date, is_pin_code_activated=is_pin_code_activated)
        try:
            user_db.update()
        except UserException as e:
            self.logger.error(e)
            http_code = HTTPStatus.BAD_REQUEST
            error = e.error
            error_code = e.error_code
            developer_message = e.developer_message
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{self.__api_url__}/uuid/{suuid}"
        return resp

    def get(self, suuid: str = None, email: str = None, pin_code: str = None) -> Response:
        super(UsersAPI, self).get(req=request)

        if suuid is not None:
            is_valid = check_uuid(suuid=suuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.USER_FINDBYPINCODE_ERROR)

        user_db = UserDB(storage_service=self.__db_storage_service, suuid=suuid, email=email, pin_code=pin_code,
                         limit=self.pagination.limit, offset=self.pagination.offset)

        if pin_code is not None:
            try:
                user = user_db.find_by_pin_code()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserException as e:
                self.logger.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except UserNotFoundException as e:
                self.logger.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp

        if suuid is None and email is None:
            # find all user is no parameter set
            try:
                user_list = user_db.find_all()
                users_dict = [user_list[i].to_api_dict() for i in range(0, len(user_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=users_dict, limit=self.pagination.limit, offset=self.pagination.offset)
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserException as e:
                self.logger.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        elif suuid is not None:
            # find user by suuid
            try:
                user = user_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserNotFoundException as e:
                self.logger.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except UserException as e:
                self.logger.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        elif email is not None:
            # find user by email
            try:
                user = user_db.find_by_email()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserNotFoundException as e:
                self.logger.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except UserException as e:
                self.logger.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        else:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.UNKNOWN_ERROR_CODE)
