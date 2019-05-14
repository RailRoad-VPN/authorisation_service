import base64
import datetime
import logging
import os
import sys
from http import HTTPStatus
from typing import List

from flask import Response, request

from app.exception import AuthError, UserTicketException, UserTicketNotFoundException
from app.model.user.ticket import TicketDB

sys.path.insert(0, '../psql_library')
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from utils import check_uuid
from response import make_api_response, make_error_request_response, check_required_api_fields
from api import ResourceAPI, APIResourceURL
from response import APIResponseStatus, APIResponse


class TicketsAPI(ResourceAPI):
    __version__ = 1

    logger = logging.getLogger(__name__)

    __endpoint_name__ = __qualname__
    __api_url__ = 'tickets'

    _config = None

    __db_storage_service = None

    @staticmethod
    def get_api_urls(base_url: str) -> List[APIResourceURL]:
        url = "%s/%s" % (base_url, TicketsAPI.__api_url__)
        api_urls = [
            APIResourceURL(base_url=url, resource_name='', methods=['GET', 'POST']),
            APIResourceURL(base_url=url, resource_name='<string:suuid_or_number>', methods=['GET', 'PUT', 'DELETE']),
        ]
        return api_urls

    def __init__(self, db_storage_service: DBStorageService, *args) -> None:
        super().__init__(*args)
        self.__db_storage_service = db_storage_service

    def post(self) -> Response:
        super(TicketsAPI, self).post(req=request)

        request_json = request.json

        if request_json is None:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.REQUEST_NO_JSON)

        user_uuid = request_json.get(TicketDB._user_uuid_field, None)
        contact_email = request_json.get(TicketDB._contact_email_field, 'anonymous')
        description = request_json.get(TicketDB._description_field, None)
        status_id = request_json.get(TicketDB._status_id_field, None)
        extra_info = request_json.get(TicketDB._extra_info_field, None)
        zipfile = request_json.get('zipfile', None)

        req_fields = {
            'status_id': status_id,
            'contact_email': contact_email,
            'description': description,
        }

        error_fields = check_required_api_fields(req_fields)
        if len(error_fields) > 0:
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=HTTPStatus.BAD_REQUEST,
                                        errors=error_fields)
            resp = make_api_response(data=response_data, http_code=response_data.code)
            return resp

        self.logger.debug("create userticketdb object")
        user_ticket_db = TicketDB(storage_service=self.__db_storage_service, user_uuid=user_uuid,
                                  extra_info=extra_info, status_id=status_id, contact_email=contact_email,
                                  description=description)
        try:
            self.logger.debug("create user ticket")
            number = user_ticket_db.create()
        except UserTicketException as e:
            self.logger.error(e)
            error_code = e.error_code
            error = e.error
            developer_message = e.developer_message
            http_code = HTTPStatus.BAD_REQUEST
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            return make_api_response(data=response_data, http_code=http_code)

        self.logger.debug("check zipfile")
        if zipfile:
            self.logger.debug("there is zipfile")

            self.logger.debug('create today date in string')
            today = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            self.logger.debug(f"Today: {today}")

            self.logger.debug("create user ticket zip dir if does not exist")
            os.makedirs(self._config['USER_TICKET_ZIP_DIR'], exist_ok=True)

            self.logger.debug("build path to zip")
            path_to_zip = f"{self._config['USER_TICKET_ZIP_DIR']}/{contact_email}"
            self.logger.debug(f"path to zip: {path_to_zip}")

            self.logger.debug("create path to zip dir if does not exist")
            os.makedirs(path_to_zip, exist_ok=True)

            self.logger.debug("build zip_path")
            zip_path = f"{path_to_zip}/{number}.zip"
            self.logger.debug(f"zip_path: {path_to_zip}")

            self.logger.debug("write zip to FS")
            try:
                self.logger.debug("base64 decode zipfile")
                zip_file_bytes = base64.b64decode(zipfile)
                with open(zip_path, 'wb') as w:
                    w.write(zip_file_bytes)

                user_ticket_db.set_zip_path(zip_path)
            except TypeError:
                self.logger.debug("TypeError when write zipfile")

        response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.CREATED)
        resp = make_api_response(data=response_data, http_code=HTTPStatus.CREATED)
        api_url = self.__api_url__
        resp.headers['Location'] = f"{self._config['API_BASE_URI']}/{api_url}/{number}"
        return resp

    def put(self, user_uuid: str, suuid: str) -> Response:
        resp = make_error_request_response(http_code=HTTPStatus.METHOD_NOT_ALLOWED)
        return resp

    def get(self, suuid_or_number: str = None) -> Response:
        super(TicketsAPI, self).get(req=request)

        ticket_number = None
        ticket_uuid = None

        user_uuid = request.args.get("user_uuid", None)

        if suuid_or_number is not None:
            self.logger.debug("get by ticket number or ticket uuid")
            is_valid = check_uuid(suuid=suuid_or_number)
            if not is_valid:
                self.logger.debug("get by ticket number")
                try:
                    ticket_number = int(suuid_or_number)
                except ValueError:
                    return make_error_request_response(HTTPStatus.BAD_REQUEST)
            else:
                ticket_uuid = suuid_or_number

            ticket_db = TicketDB(storage_service=self.__db_storage_service, suuid=ticket_uuid,
                                 number=ticket_number, user_uuid=user_uuid,
                                 limit=self.pagination.limit, offset=self.pagination.offset)

            if ticket_uuid is not None:
                # find ticket by suuid
                try:
                    ticket = ticket_db.find_by_suuid()
                    response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                                data=ticket.to_api_dict())
                    resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                    return resp
                except UserTicketNotFoundException as e:
                    self.logger.error(e)
                    http_code = HTTPStatus.NOT_FOUND
                    error = e.error
                    error_code = e.error_code
                    developer_message = e.developer_message
                    response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                                developer_message=developer_message, error=error, error_code=error_code)
                    resp = make_api_response(data=response_data, http_code=http_code)
                    return resp
                except UserTicketException as e:
                    self.logger.error(e)
                    http_code = HTTPStatus.BAD_REQUEST
                    error = e.error
                    error_code = e.error_code
                    developer_message = e.developer_message
                    response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                                developer_message=developer_message, error=error, error_code=error_code)
                    resp = make_api_response(data=response_data, http_code=http_code)
                    return resp
            elif ticket_number is not None:
                # find ticket by number
                try:
                    ticket = ticket_db.find_by_ticket_number()
                    response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                                data=ticket.to_api_dict())
                    resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                    return resp
                except UserTicketNotFoundException as e:
                    self.logger.error(e)
                    http_code = HTTPStatus.NOT_FOUND
                    error = e.error
                    error_code = e.error_code
                    developer_message = e.developer_message
                    response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                                developer_message=developer_message, error=error, error_code=error_code)
                    resp = make_api_response(data=response_data, http_code=http_code)
                    return resp
                except UserTicketException as e:
                    self.logger.error(e)
                    http_code = HTTPStatus.BAD_REQUEST
                    error = e.error
                    error_code = e.error_code
                    developer_message = e.developer_message
                    response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code,
                                                developer_message=developer_message, error=error, error_code=error_code)
                    resp = make_api_response(data=response_data, http_code=http_code)
                    return resp
        elif user_uuid:
            self.logger.debug("get all user tickets")

            is_valid = check_uuid(suuid=user_uuid)
            if not is_valid:
                return make_error_request_response(HTTPStatus.NOT_FOUND, err=AuthError.BAD_USER_IDENTITY)

            ticket_db = TicketDB(storage_service=self.__db_storage_service, suuid=ticket_uuid,
                                 number=ticket_number, user_uuid=user_uuid,
                                 limit=self.pagination.limit, offset=self.pagination.offset)
            # find all user tickets is no parameter set
            try:
                user_ticket_list = ticket_db.find_by_user_uuid()
                user_ticket_list_dict = [user_ticket_list[i].to_api_dict() for i in range(0, len(user_ticket_list))]
                response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK,
                                            data=user_ticket_list_dict, limit=self.pagination.limit,
                                            offset=self.pagination.offset)
                resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
                return resp
            except UserTicketException as e:
                self.logger.error(e)
                http_code = HTTPStatus.BAD_REQUEST
                error = e.error
                error_code = e.error_code
                developer_message = e.developer_message
                response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                            developer_message=developer_message, error_code=error_code)
                resp = make_api_response(data=response_data, http_code=http_code)
                return resp
        else:
            return make_error_request_response(HTTPStatus.BAD_REQUEST, err=AuthError.UNKNOWN_ERROR_CODE)

    def delete(self, user_uuid: str, suuid: str) -> Response:
        is_valid_a = check_uuid(suuid=suuid)
        is_valid_b = check_uuid(suuid=user_uuid)
        if not is_valid_a or not is_valid_b:
            return make_error_request_response(HTTPStatus.NOT_FOUND, err=AuthError.BAD_IDENTITY_ERROR)

        user_ticket_db = TicketDB(storage_service=self.__db_storage_service, suuid=suuid, user_uuid=user_uuid)
        try:
            user_ticket_db.delete()
            response_data = APIResponse(status=APIResponseStatus.success.status, code=HTTPStatus.OK)
            resp = make_api_response(data=response_data, http_code=HTTPStatus.OK)
            return resp
        except UserTicketException as e:
            self.logger.error(e)
            http_code = HTTPStatus.BAD_REQUEST
            error = e.error
            error_code = e.error_code
            developer_message = e.developer_message
            response_data = APIResponse(status=APIResponseStatus.failed.status, code=http_code, error=error,
                                        developer_message=developer_message, error_code=error_code)
            resp = make_api_response(data=response_data, http_code=http_code)
            return resp
