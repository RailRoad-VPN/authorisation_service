import datetime
import logging
import sys
import uuid as uuidlib
from typing import List, Optional

from psycopg2._psycopg import DatabaseError

from app.exception import UserDeviceException, AuthError, UserDeviceNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserDevice(object):
    __version__ = 1

    _suuid = None
    _user_uuid = None
    _device_token = None
    _device_id = None
    _device_os = None
    _location = None
    _is_active = None
    _modify_reason = None
    _modify_date = None
    _created_date = None

    def __init__(self, suuid: str = None, user_uuid: str = None, device_token: str = None,
                 device_id: str = None, device_os: str = None, location: str = None, is_active: bool = None, modify_reason: str = None,
                 modify_date: datetime = None, created_date: datetime = None):
        self._suuid = suuid
        self._user_uuid = user_uuid
        self._device_token = device_token
        self._device_id = device_id
        self._device_os = device_os
        self._location = location
        self._is_active = is_active
        self._modify_reason = modify_reason
        self._modify_date = modify_date
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'device_token': self._device_token,
            'device_id': self._device_id,
            'device_os': self._device_os,
            'location': self._location,
            'is_active': self._is_active,
            'modify_reason': self._modify_reason,
            'modify_date': str(self._modify_date),
            'created_date': str(self._created_date),
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'device_token': self._device_token,
            'device_id': self._device_id,
            'device_os': self._device_os,
            'location': self._location,
            'is_active': self._is_active,
            'modify_reason': self._modify_reason,
            'modify_date': str(self._modify_date),
            'created_date': str(self._created_date),
        }


class UserDeviceStored(StoredObject, UserDevice):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, user_uuid: str = None,
                 device_token: str = None, device_id: str = None, device_os: str = None, location: str = None, is_active: bool = None,
                 modify_reason: str = None, created_date: datetime = None, limit: int = None, offset: int = None,
                 **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserDevice.__init__(self, suuid=suuid, user_uuid=user_uuid, device_token=device_token,
                            device_id=device_id, device_os=device_os, location=location, is_active=is_active,
                            modify_reason=modify_reason, created_date=created_date)


class UserDeviceDB(UserDeviceStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _user_uuid_field = 'user_uuid'
    _device_token_field = 'device_token'
    _device_id_field = 'device_id'
    _device_os_field = 'device_os'
    _location_field = 'location'
    _is_active_field = 'is_active'
    _modify_reason_field = 'modify_reason'
    _modify_date_field = 'modify_date'
    _created_date_field = 'created_date'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self) -> str:
        self._suuid = uuidlib.uuid4()
        logging.info('Create object UserDevice with uuid: ' + str(self._suuid))
        create_user_device_sql = '''
                          INSERT INTO public.user_device 
                            (
                                uuid,
                                user_uuid,
                                device_token,
                                device_id,
                                device_os,
                                location,
                                is_active
                            ) 
                          VALUES 
                            (?, ?, ?, ?, ?, ?, ?)
        '''
        create_user_device_params = (
            self._suuid,
            self._user_uuid,
            self._device_token,
            self._device_id,
            self._device_os,
            self._location,
            self._is_active,
        )
        logging.debug('Create UserDevice SQL : %s' % create_user_device_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(sql=create_user_device_sql, data=create_user_device_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_DEVICE_CREATE_ERROR_DB.message
            error_code = AuthError.USER_DEVICE_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('UserDevice created.')

        return self._suuid

    def update(self):
        logging.info('Update UserDevice')

        update_sql = '''
                    UPDATE 
                      public.user_device 
                    SET 
                      user_uuid = ?,
                      device_token = ?,
                      device_id = ?,
                      device_os = ?,
                      location = ?,
                      is_active = ?,
                      modify_reason = ?
                    WHERE 
                      uuid = ?;
        '''

        logging.debug('Update SQL: %s' % update_sql)

        params = (
            self._user_uuid,
            self._device_token,
            self._device_id,
            self._device_os,
            self._location,
            self._is_active,
            self._modify_reason,
            self._suuid,
        )
        try:
            logging.debug("Call database service")
            self._storage_service.update(update_sql, params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_DEVICE_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_DEVICE_UPDATE_ERROR_DB.code
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

    def find_by_suuid(self) -> Optional[UserDevice]:
        logging.info('Find UserDevice by uuid')
        select_sql = '''
                        SELECT 
                            uuid,
                            user_uuid,
                            device_token,
                            device_id,
                            device_os,
                            location,
                            is_active,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.user_device 
                        WHERE 
                            uuid = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            user_device_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_DEVICE_FINDBYUUID_ERROR_DB.message
            error_code = AuthError.USER_DEVICE_FINDBYUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_FINDBYUUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_device_list_db) == 1:
            user_device_db = user_device_list_db[0]
        elif len(user_device_list_db) == 0:
            error_message = AuthError.USER_DEVICE_FINDBYUUID_ERROR.message
            error_code = AuthError.USER_DEVICE_FINDBYUUID_ERROR.code
            developer_message = AuthError.USER_DEVICE_FINDBYUUID_ERROR.developer_message
            raise UserDeviceNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = AuthError.USER_DEVICE_FINDBYUUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYUUID_ERROR.developer_message
            error_code = AuthError.USER_DEVICE_FINDBYUUID_ERROR.code
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_user_devicedb_to_user_device(user_device_db=user_device_db)

    def find_by_device_token(self) -> Optional[UserDevice]:
        logging.info('Find UserDevice by device_token')
        select_sql = '''
                        SELECT 
                            uuid,
                            user_uuid,
                            device_token,
                            device_id,
                            device_os,
                            location,
                            is_active,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.user_device 
                        WHERE 
                            device_token = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._device_token,)

        try:
            logging.debug('Call database service')
            user_device_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR_DB.message
            error_code = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_device_list_db) == 1:
            user_device_db = user_device_list_db[0]
        elif len(user_device_list_db) == 0:
            error_message = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.message
            error_code = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.code
            developer_message = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.developer_message
            raise UserDeviceNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.message
            developer_message = "%s. Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.developer_message
            error_code = AuthError.USER_DEVICE_FINDBYDEVICETOKEN_ERROR.code
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_user_devicedb_to_user_device(user_device_db=user_device_db)

    def find_by_user_uuid(self) -> Optional[UserDevice]:
        logging.info('Find UserDevice by device_token')
        select_sql = '''
                        SELECT 
                            uuid,
                            user_uuid,
                            device_token,
                            device_id,
                            device_os,
                            location,
                            is_active,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.user_device 
                        WHERE 
                            user_uuid = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._user_uuid,)

        try:
            logging.debug('Call database service')
            user_device_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR_DB.message
            error_code = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_device_list_db) == 1:
            user_device_db = user_device_list_db[0]
        elif len(user_device_list_db) == 0:
            error_message = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.message
            error_code = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.code
            developer_message = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.developer_message
            raise UserDeviceNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.message
            developer_message = "%s. Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.developer_message
            error_code = AuthError.USER_DEVICE_FINDBYUSERUUID_ERROR.code
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_user_devicedb_to_user_device(user_device_db=user_device_db)

    def find_all(self) -> Optional[List[UserDevice]]:
        logging.info('Find all UserDevices')
        select_sql = '''
                        SELECT 
                            uuid,
                            user_uuid,
                            device_token,
                            device_id,
                            device_os,
                            location,
                            is_active,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.user_device 
                    '''
        if self._limit:
            select_sql += "LIMIT %s\nOFFSET %s" % (self._limit, self._offset)
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            user_device_db_list = self._storage_service.get(select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_DEVICE_FINDALL_ERROR_DB.message
            error_code = AuthError.USER_DEVICE_FINDALL_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_DEVICE_FINDALL_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserDeviceException(error=error_message, error_code=error_code, developer_message=developer_message)
        user_device_list = []

        for user_device_db in user_device_db_list:
            user_device = self.__map_user_devicedb_to_user_device(user_device_db=user_device_db)
            user_device_list.append(user_device)

        if len(user_device_list) == 0:
            logging.warning('Empty UserDevice list of method find_all. Very strange behaviour.')

        return user_device_list

    def __map_user_devicedb_to_user_device(self, user_device_db):
        return UserDevice(suuid=user_device_db[self._suuid_field], user_uuid=user_device_db[self._user_uuid_field],
                          device_token=user_device_db[self._device_token_field],
                          device_id=user_device_db[self._device_id_field],
                          device_os=user_device_db[self._device_os_field],
                          location=user_device_db[self._location_field],
                          is_active=user_device_db[self._is_active_field],
                          modify_reason=user_device_db[self._modify_reason_field],
                          modify_date=user_device_db[self._modify_date_field],
                          created_date=user_device_db[self._created_date_field])
