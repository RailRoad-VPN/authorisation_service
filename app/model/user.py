import datetime
import logging
import sys
import uuid as uuidlib
from typing import List, Optional

from psycopg2._psycopg import DatabaseError

from app.exception import UserException, AuthError, UserNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService


class User(object):
    __version__ = 1

    _uuid = None
    _email = None
    _created_date = None
    _password = None
    _account_non_expired = False
    _account_non_locked = False
    _credentials_non_expired = False
    _enabled = False

    def __init__(self, uuid: str, email: str, created_date: datetime, password: str,
                 account_non_expired: bool, account_non_locked: bool, credentials_non_expired: bool, enabled: bool):
        self._uuid = uuid
        self._email = email
        self._created_date = created_date
        self._password = password
        self._account_non_expired = account_non_expired
        self._account_non_locked = account_non_locked
        self._credentials_non_expired = credentials_non_expired
        self._enabled = enabled

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'email': self._email,
            'created_date': self._created_date,
            'password': self._password,
            'account_non_expired': self._account_non_expired,
            'account_non_locked': self._account_non_locked,
            'credentials_non_expired': self._credentials_non_expired,
            'enabled': self._enabled,
        }


class UserStored(User):
    __version__ = 1

    _storage_service = None

    def __init__(self, storage_service: StorageService, **kwargs: dict) -> None:
        super().__init__(**kwargs)

        self._storage_service = storage_service


class UserDB(UserStored):
    __version__ = 1

    __uuid_field = 'uuid'
    __email_field = 'email'
    __created_date_field = 'created_date'
    __password_field = 'password'
    __account_non_expired_field = 'account_non_expired'
    __account_non_locked_field = 'account_non_locked'
    __credentials_non_expired_field = 'credentials_non_expired'
    __enabled_field = 'enabled'

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)

    def create(self) -> str:
        self._uuid = uuidlib.uuid4()
        logging.info('Create object User with uuid: ' + str(self._uuid))
        create_user_sql = 'INSERT INTO public."user" (uuid, email, password, enabled, account_non_expired, ' \
                          'account_non_locked, credentials_non_expired) VALUES (?, ?, ?, ?, ?, ?, ?)'
        create_user_params = (
            self._uuid,
            self._email,
            self._password,
            self._enabled,
            self._account_non_expired,
            self._account_non_locked,
            self._credentials_non_expired
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
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_CREATE_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)
        logging.debug('User created.')

        return self._uuid

    def update(self):
        # TODO update user social network
        logging.info('Update User')

        update_sql = '''
                    UPDATE public."user" 
                    SET email = ?,
                      enabled = ?,
                      password = ?, 
                      account_non_expired = ?, 
                      account_non_locked = ?, 
                      credentials_non_expired = ?
                    WHERE 
                      uuid = ?;
        '''

        logging.debug('Update SQL: %s' % update_sql)

        params = (
            self._email, self._password, self._enabled, self._account_non_expired,
            self._account_non_locked, self._credentials_non_expired, self._uuid
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
            code = e.pgcode
            error_message = 'Internal database error'
            developer_message = "DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (e.pgcode, e.pgerror)
            system_error_code = AuthError.USER_UPDATE_ERROR_DB
            data = {
                'code': code,
                'message': error_message,
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

    def find_by_uuid(self) -> Optional[User]:
        logging.info('Find User by uuid')
        select_sql = 'SELECT * FROM public."user" WHERE uuid = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._uuid,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDBYUUID_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = "User not found"
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': None
            }
            raise UserNotFoundException(message=error_message, code=system_error_code, data=data)
        else:
            error_message = "User not found"
            developer_message = "Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database."
            system_error_code = AuthError.USER_FINDBYUUID_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=system_error_code, data=data)

        return self.__map_userdb_to_user(user_db)

    def find_by_email(self) -> Optional[User]:
        logging.info('Find User by email')
        select_sql = 'SELECT * FROM public."user" WHERE email = ?'
        logging.debug('Select SQL: %s' % select_sql)
        params = (self._email,)

        try:
            logging.debug('Call database service')
            user_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = "User not found"
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': None
            }
            raise UserNotFoundException(message=error_message, code=system_error_code, data=data)
        else:
            error_message = "User not found"
            developer_message = "Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database."
            system_error_code = AuthError.USER_FINDBYEMAIL_ERROR
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=system_error_code, data=data)

        return self.__map_userdb_to_user(user_db)

    def find_all(self) -> Optional[List[User]]:
        logging.info('Find all Users')
        select_sql = 'SELECT * FROM public."user"'
        logging.debug('Select SQL: %s' % select_sql)

        try:
            logging.debug('Call database service')
            user_db_list = self._storage_service.get(select_sql)
        except DatabaseError as e:
            logging.error(e)
            code = e.pgcode
            error_message = 'Internal system error'
            system_error_code = AuthError.USER_FINDALL_ERROR_DB
            developer_message = 'DatabaseError: %s . Something wrong with database or SQL is broken.' % e.pgerror
            data = {
                'system_error_code': system_error_code,
                'developer_message': developer_message
            }
            raise UserException(message=error_message, code=code, data=data)
        user_list = []

        for user_db in user_db_list:
            user = self.__map_userdb_to_user(user_db)
            user_list.append(user)

        if len(user_list) == 0:
            logging.warning('Empty User list of method find_all. Very strange behaviour.')

        return user_list

    def __map_userdb_to_user(self, user_db):
        self._uuid = user_db[self.__uuid_field]
        return User(uuid=self._uuid,
                    email=user_db[self.__email_field],
                    account_non_expired=user_db[self.__account_non_expired_field],
                    account_non_locked=user_db[self.__account_non_locked_field],
                    credentials_non_expired=user_db[self.__credentials_non_expired_field],
                    created_date=user_db[self.__created_date_field],
                    password=user_db[self.__password_field],
                    enabled=user_db[self.__enabled_field])
