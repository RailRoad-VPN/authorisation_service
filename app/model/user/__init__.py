import datetime
import logging
import sys
import uuid as uuidlib
from typing import List, Optional

from psycopg2._psycopg import DatabaseError

from app.exception import UserException, AuthError, UserNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class User(object):
    __version__ = 1

    _suuid = None
    _email = None
    _created_date = None
    _password = None
    _is_expired = None
    _is_locked = None
    _is_password_expired = None
    _enabled = None
    _pin_code = None
    _pin_code_expire_date = None
    _modify_date = None
    _modify_reason = None
    _is_pin_code_activated = None

    def __init__(self, suuid: str = None, email: str = None, created_date: datetime = None, password: str = None,
                 is_expired: bool = False, is_locked: bool = False, is_password_expired: bool = False,
                 enabled: bool = False, pin_code: int = None, pin_code_expire_date: datetime = None,
                 modify_date: datetime = None, modify_reason: str = None, is_pin_code_activated: bool = False):
        self._suuid = suuid
        self._email = email
        self._created_date = created_date
        self._password = password
        self._is_expired = is_expired
        self._is_locked = is_locked
        self._is_password_expired = is_password_expired
        self._enabled = enabled
        self._pin_code = pin_code
        self._pin_code_expire_date = pin_code_expire_date
        self._modify_date = modify_date
        self._modify_reason = modify_reason
        self._is_pin_code_activated = is_pin_code_activated

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'email': self._email,
            'created_date': self._created_date,
            'password': self._password,
            'is_expired': self._is_expired,
            'is_locked': self._is_locked,
            'is_password_expired': self._is_password_expired,
            'enabled': self._enabled,
            'pin_code': self._pin_code,
            'pin_code_expire_date': self._pin_code_expire_date,
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'is_pin_code_activated': self._is_pin_code_activated,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'email': self._email,
            'created_date': self._created_date,
            'password': self._password,
            'is_expired': self._is_expired,
            'is_locked': self._is_locked,
            'is_password_expired': self._is_password_expired,
            'enabled': self._enabled,
            'pin_code': self._pin_code,
            'pin_code_expire_date': self._pin_code_expire_date,
            'modify_date': self._modify_date,
            'modify_reason': self._modify_reason,
            'is_pin_code_activated': self._is_pin_code_activated,
        }


class UserStored(StoredObject, User):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, email: str = None,
                 created_date: datetime = None, password: str = None, is_expired: bool = False, is_locked: bool = False,
                 is_password_expired: bool = False, enabled: bool = False, pin_code: int = None,
                 pin_code_expire_date: datetime = None, modify_date: datetime = None, modify_reason: str = None,
                 is_pin_code_activated=False, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        User.__init__(self, suuid=suuid, email=email, created_date=created_date, password=password,
                      is_expired=is_expired, is_locked=is_locked, is_password_expired=is_password_expired,
                      enabled=enabled, pin_code=pin_code, pin_code_expire_date=pin_code_expire_date,
                      modify_date=modify_date, modify_reason=modify_reason, is_pin_code_activated=is_pin_code_activated)


class UserDB(UserStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _email_field = 'email'
    _created_date_field = 'created_date'
    _password_field = 'password'
    _is_expired_field = 'is_expired'
    _is_locked_field = 'is_locked'
    _is_password_expired_field = 'is_password_expired'
    _enabled_field = 'enabled'
    _pin_code_field = 'pin_code'
    _pin_code_expire_date_field = 'pin_code_expire_date'
    _modify_date_field = 'modify_date'
    _modify_reason_field = 'modify_reason'
    _is_pin_code_activated_field = 'is_pin_code_activated'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self) -> str:
        self._suuid = uuidlib.uuid4()
        logging.info('Create object User with uuid: ' + str(self._suuid))
        create_user_sql = '''
                          INSERT INTO public."user" 
                            (
                                uuid, 
                                email, 
                                password, 
                                enabled, 
                                is_expired, 
                                is_locked, 
                                is_password_expired,
                                pin_code,
                                pin_code_expire_date,
                                is_pin_code_activated
                            ) 
                          VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        create_user_params = (
            self._suuid,
            self._email,
            self._password,
            self._enabled,
            self._is_expired,
            self._is_locked,
            self._is_password_expired,
            self._pin_code,
            self._pin_code_expire_date,
            self._is_pin_code_activated,
        )
        logging.debug('Create User SQL : %s' % create_user_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(create_user_sql, create_user_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_CREATE_ERROR_DB.message
            error_code = AuthError.USER_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('User created.')

        return self._suuid

    def update(self):
        self._modify_date = datetime.datetime.now()
        logging.info('Update User')

        update_sql = '''
                    UPDATE 
                      public."user" 
                    SET 
                      email = ?,
                      password = ?, 
                      enabled = ?,
                      is_expired = ?, 
                      is_locked = ?, 
                      is_password_expired = ?,
                      pin_code = ?,
                      pin_code_expire_date = ?,
                      modify_reason = ?,
                      is_pin_code_activated = ?
                    WHERE 
                      uuid = ?;
        '''

        logging.debug('Update SQL: %s' % update_sql)

        params = (
            self._email,
            self._password,
            self._enabled,
            self._is_expired,
            self._is_locked,
            self._is_password_expired,
            self._pin_code,
            self._pin_code_expire_date,
            self._modify_reason,
            self._is_pin_code_activated,
            self._suuid
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
            error_message = AuthError.USER_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_UPDATE_ERROR_DB.code
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

    def find_by_suuid(self) -> Optional[User]:
        logging.info('Find User by uuid')
        select_sql = '''
                        SELECT 
                            uuid,
                            email,
                            to_json(created_date) AS created_date,
                            password,
                            is_expired,
                            is_locked,
                            is_password_expired,
                            enabled,
                            pin_code,
                            to_json(pin_code_expire_date) AS pin_code_expire_date,
                            to_json(modify_date) AS modify_date,
                            modify_reason,
                            is_pin_code_activated
                        FROM 
                            public."user" 
                        WHERE 
                            uuid = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_FINDBYUUID_ERROR_DB.message
            error_code = AuthError.USER_FINDBYUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_FINDBYUUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = AuthError.USER_FINDBYUUID_ERROR.message
            error_code = AuthError.USER_FINDBYUUID_ERROR.code
            developer_message = AuthError.USER_FINDBYUUID_ERROR.developer_message
            raise UserNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_FINDBYUUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYUUID_ERROR.developer_message
            error_code = AuthError.USER_FINDBYUUID_ERROR.code
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_userdb_to_user(user_db)

    def find_by_email(self) -> Optional[User]:
        logging.info('Find User by email')
        select_sql = '''
                        SELECT 
                            uuid,
                            email,
                            to_json(created_date) AS created_date,
                            password,
                            is_expired,
                            is_locked,
                            is_password_expired,
                            enabled,
                            pin_code,
                            to_json(pin_code_expire_date) AS pin_code_expire_date,
                            to_json(modify_date) AS modify_date,
                            modify_reason,
                            is_pin_code_activated
                        FROM 
                            public."user" 
                        WHERE 
                            email = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._email,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_FINDBYEMAIL_ERROR_DB.message
            error_code = AuthError.USER_FINDBYEMAIL_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_FINDBYEMAIL_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = AuthError.USER_FINDBYEMAIL_ERROR.message
            error_code = AuthError.USER_FINDBYEMAIL_ERROR.code
            developer_message = AuthError.USER_FINDBYEMAIL_ERROR.developer_message
            raise UserNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_FINDBYEMAIL_ERROR.message
            developer_message = "%s. Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYEMAIL_ERROR.developer_message
            error_code = AuthError.USER_FINDBYEMAIL_ERROR.code
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_userdb_to_user(user_db)

    def find_by_pin_code(self) -> Optional[User]:
        logging.info('Find User by pin_code')
        select_sql = '''
                        SELECT 
                            uuid,
                            email,
                            to_json(created_date) AS created_date,
                            password,
                            is_expired,
                            is_locked,
                            is_password_expired,
                            enabled,
                            pin_code,
                            to_json(pin_code_expire_date) AS pin_code_expire_date,
                            to_json(modify_date) AS modify_date,
                            modify_reason,
                            is_pin_code_activated
                        FROM 
                            public."user" 
                        WHERE 
                            pin_code = ?
                    '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._pin_code,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_FINDBYPINCODE_ERROR_DB.message
            error_code = AuthError.USER_FINDBYPINCODE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_FINDBYPINCODE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = AuthError.USER_FINDBYPINCODE_ERROR.message
            error_code = AuthError.USER_FINDBYPINCODE_ERROR.code
            developer_message = AuthError.USER_FINDBYPINCODE_ERROR.developer_message
            raise UserNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_FINDBYPINCODE_ERROR.message
            developer_message = "%s. Find by specified pin_code return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYPINCODE_ERROR.developer_message
            error_code = AuthError.USER_FINDBYPINCODE_ERROR.code
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_userdb_to_user(user_db)

    def find_all(self) -> Optional[List[User]]:
        logging.info('Find all Users')
        select_sql = '''
                        SELECT 
                            uuid,
                            email,
                            to_json(created_date) AS created_date,
                            password,
                            is_expired,
                            is_locked,
                            is_password_expired,
                            enabled,
                            pin_code,
                            to_json(pin_code_expire_date) AS pin_code_expire_date,
                            to_json(modify_date) AS modify_date,
                            modify_reason,
                            is_pin_code_activated
                        FROM 
                            public."user" 
                    '''
        if self._limit:
            select_sql += f"\nLIMIT {self._limit}\nOFFSET {self._offset}"
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            user_db_list = self._storage_service.get(select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_FINDALL_ERROR_DB.message
            error_code = AuthError.USER_FINDALL_ERROR_DB.code
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_FINDALL_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)
        user_list = []

        for user_db in user_db_list:
            user = self.__map_userdb_to_user(user_db)
            user_list.append(user)

        if len(user_list) == 0:
            logging.warning('Empty User list of method find_all. Very strange behaviour.')

        return user_list

    def __map_userdb_to_user(self, user_db):
        return User(suuid=user_db[self._suuid_field], email=user_db[self._email_field],
                    is_expired=user_db[self._is_expired_field], is_locked=user_db[self._is_locked_field],
                    is_password_expired=user_db[self._is_password_expired_field],
                    created_date=user_db[self._created_date_field], password=user_db[self._password_field],
                    enabled=user_db[self._enabled_field], pin_code=user_db[self._pin_code_field],
                    pin_code_expire_date=user_db[self._pin_code_expire_date_field],
                    is_pin_code_activated=user_db[self._is_pin_code_activated_field])
