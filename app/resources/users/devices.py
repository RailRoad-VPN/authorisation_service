import logging
import sys
import uuid
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import AuthError, UserDeviceException, UserDeviceNotFoundException
from app.model.user.device import UserDeviceDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI
from response import APIResponseStatus, APIResponse
from rest import APIResourceURL


class UsersDevicesAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'users/<string:user_uuid>/devices'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, UsersDevicesAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid>', methods=['GET', 'PUT', 'DELETE']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self, user_uuid: str) -> Response:
        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.REQUEST_NO_JSON)

        device_id = request_json.get(UserDeviceDB._device_id_field, None)
        platform_id = request_json.get(UserDeviceDB._platform_id_field, None)
        vpn_type_id = request_json.get(UserDeviceDB._vpn_type_id_field, None)
        location = request_json.get(UserDeviceDB._location_field, None)
        is_active = request_json.get(UserDeviceDB._is_active_field, True)
        virtual_ip = request_json.get(UserDeviceDB._virtual_ip_field, None)
        device_ip = request_json.get(UserDeviceDB._device_ip_field, None)
        connected_since = request_json.get(UserDeviceDB._connected_since_field, None)

        req_fields = {
            'user_uuid': user_uuid,
            'device_id': device_id,
            'platform_id': platform_id,
            'vpn_type_id': vpn_type_id,
            'is_active': is_active
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        device_token = uuid.uuid4().hex

        user_device_db = UserDeviceDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                      device_id=device_id, device_token=device_token, location=location,
                                      platform_id=platform_id, vpn_type_id=vpn_type_id, is_active=is_active,
                                      connected_since=connected_since, virtual_ip=virtual_ip, device_ip=device_ip)
        try:
            suuid = user_device_db.create()
        except UserDeviceException as e:
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
        api_url = self.__api_url__.replace('<string:user_uuid>', user_uuid)
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{api_url}/{suuid}"
        resp.headers['X-Device-Token'] = device_token
        return resp

    def put(self, user_uuid: str, suuid: str) -> Response:
        request_json = request.json

        suuid_b = request_json.get(UserDeviceDB._suuid_field, None)
        user_uuid_b = request_json.get(UserDeviceDB._user_uuid_field, None)

        is_valid_uuid = check_uuid(suuid=suuid)
        is_valid_uuid_b = check_uuid(suuid=suuid_b)
        is_valid_user_uuid = check_uuid(suuid=user_uuid)
        is_valid_user_uuid_b = check_uuid(suuid=user_uuid_b)
        if not is_valid_user_uuid or not is_valid_user_uuid_b or not is_valid_uuid or not is_valid_uuid_b \
                or user_uuid != user_uuid_b:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.USER_DEVICE_FINDBYUUID_ERROR)

        device_id = request_json.get(UserDeviceDB._device_id_field, None)
        device_ip = request_json.get(UserDeviceDB._device_ip_field, None)
        location = request_json.get(UserDeviceDB._location_field, None)
        is_active = request_json.get(UserDeviceDB._is_active_field, None)
        modify_reason = request_json.get(UserDeviceDB._modify_reason_field, None)

        req_fields = {
            'device_id': device_id,
            'is_active': is_active,
            'modify_reason': modify_reason,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        user_device_db = UserDeviceDB(storage_service=self.__db_storage_service, suuid=suuid, user_uuid=user_uuid,
                                      device_id=device_id, location=location, is_active=is_active,
                                      device_ip=device_ip,
                                      modify_reason=modify_reason)
        try:
            if device_id is not None and device_ip is not None and location is not None:
                user_device_db.update()
            else:
                user_device_db.update_active()
        except UserDeviceException as e:
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
        resp = make_api_response(http_code=HTTPStatus.OK, data=response_data)
        api_url = self.__api_url__.replace('<string:user_uuid>', user_uuid)
        resp.headers['Location'] = '%s/%s/%s' % (self._config['API_BASE_URI'], api_url, suuid)
        return resp

    def get(self, user_uuid: str, suuid: str = None) -> Response:
        super(UsersDevicesAPI, self).get(req=request)

        is_valid = check_uuid(suuid=user_uuid)
        if not is_valid:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.USER_DEVICE_FINDBYUUID_ERROR)

        user_device_db = UserDeviceDB(storage_service=self.__db_storage_service, suuid=suuid,  device_id=suuid,
                                      user_uuid=user_uuid, limit=self.pagination.limit, offset=self.pagination.offset)
        if suuid is None:
            # find all user devices is no parameter set
            try:
                user_device_list = user_device_db.find_by_user_uuid()
                user_device_list_dict = [user_device_list[i].to_api_dict() for i in range(0, len(user_device_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_device_list_dict, limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserDeviceException as e:
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
            is_valid = check_uuid(suuid=suuid)
            # find user device by suuid
            try:
                if not is_valid:
                    user_device = user_device_db.find_by_device_id()
                else:
                    user_device = user_device_db.find_by_suuid()
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_device.to_api_dict())
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserDeviceNotFoundException as e:
                self.logger.error(e)
                http_code = HTTPStatus.NOT_FOUND
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                            developer_message=developer_message, error=error, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
            except UserDeviceException as e:
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

    def delete(self, user_uuid: str, suuid: str) -> Response:
        is_valid_a = check_uuid(suuid=suuid)
        is_valid_b = check_uuid(suuid=user_uuid)
        if not is_valid_a or not is_valid_b:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=AuthError.BAD_IDENTITY_ERROR)

        user_device_db = UserDeviceDB(storage_service=self.__db_storage_service, suuid=suuid, user_uuid=user_uuid)
        try:
            user_device_db.delete()
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
            return resp
        except UserDeviceException as e:
            self.logger.error(e)
            http_code = HTTPStatus.BAD_REQUEST
            error = e.error
            error_code = e.error_code
            developer_message = e.developer_message
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp
