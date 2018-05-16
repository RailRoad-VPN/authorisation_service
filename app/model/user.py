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
    _is_expired = None
    _is_locked = None
    _is_password_expired = None
    _enabled = None

    def __init__(self, uuid: str = None, email: str = None, created_date: datetime = None, password: str = None,
                 is_expired: bool = None, is_locked: bool = None,
                 is_password_expired: bool = None, enabled: bool = None):
        self._uuid = uuid
        self._email = email
        self._created_date = created_date
        self._password = password
        self._is_expired = is_expired
        self._is_locked = is_locked
        self._is_password_expired = is_password_expired
        self._enabled = enabled

    def to_dict(self):
        return {
            'uuid': self._uuid,
            'email': self._email,
            'created_date': self._created_date,
            'password': self._password,
            'is_expired': self._is_expired,
            'is_locked': self._is_locked,
            'is_password_expired': self._is_password_expired,
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

    _uuid_field = 'uuid'
    _email_field = 'email'
    _created_date_field = 'created_date'
    _password_field = 'password'
    _is_expired_field = 'is_expired'
    _is_locked_field = 'is_locked'
    _is_password_expired_field = 'is_password_expired'
    _enabled_field = 'enabled'

    @property
    def uuid_field(self):
        return type(self)._uuid_field

    @property
    def email_field(self):
        return type(self)._email_field

    @property
    def created_date_field(self):
        return type(self)._created_date_field

    @property
    def password_field(self):
        return type(self)._password_field

    @property
    def is_expired_field(self):
        return type(self)._is_expired_field

    @property
    def is_locked_field(self):
        return type(self)._is_locked_field

    @property
    def is_password_expired_field(self):
        return type(self)._is_password_expired_field

    @property
    def enabled_field(self):
        return type(self)._enabled_field

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)

    def create(self) -> str:
        self._uuid = uuidlib.uuid4()
        logging.info('Create object User with uuid: ' + str(self._uuid))
        create_user_sql = 'INSERT INTO public."user" (uuid, email, password, enabled, is_expired, ' \
                          'is_locked, is_password_expired) VALUES (?, ?, ?, ?, ?, ?, ?)'
        create_user_params = (
            self._uuid,
            self._email,
            self._password,
            self._enabled,
            self._is_expired,
            self._is_locked,
            self._is_password_expired
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
            error_message = AuthError.USER_CREATE_ERROR_DB.phrase
            error_code = AuthError.USER_CREATE_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (AuthError.USER_CREATE_ERROR_DB.description, e.pgcode, e.pgerror)

            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)
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
                      is_expired = ?, 
                      is_locked = ?, 
                      is_password_expired = ?
                    WHERE 
                      uuid = ?;
        '''

        logging.debug('Update SQL: %s' % update_sql)

        params = (
            self._email, self._password, self._enabled, self._is_expired,
            self._is_locked, self._is_password_expired, self._uuid
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
            error_message = AuthError.USER_UPDATE_ERROR_DB.phrase
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (AuthError.USER_UPDATE_ERROR_DB.description, e.pgcode, e.pgerror)
            error_code = AuthError.USER_UPDATE_ERROR_DB.value
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

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
            error_message = AuthError.USER_FINDBYUUID_ERROR_DB.phrase
            error_code = AuthError.USER_FINDBYUUID_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (AuthError.USER_FINDBYUUID_ERROR_DB.description, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = AuthError.USER_FINDBYUUID_ERROR.phrase
            error_code = AuthError.USER_FINDBYUUID_ERROR.value
            developer_message = AuthError.USER_FINDBYUUID_ERROR.description
            raise UserNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_FINDBYUUID_ERROR.phrase
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYUUID_ERROR.description
            error_code = AuthError.USER_FINDBYUUID_ERROR.value
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

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
            error_message = AuthError.USER_FINDBYEMAIL_ERROR_DB.phrase
            error_code = AuthError.USER_FINDBYEMAIL_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (AuthError.USER_FINDBYEMAIL_ERROR_DB.description, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_list_db) == 1:
            user_db = user_list_db[0]
        elif len(user_list_db) == 0:
            error_message = AuthError.USER_FINDBYEMAIL_ERROR.phrase
            error_code = AuthError.USER_FINDBYEMAIL_ERROR.value
            developer_message = AuthError.USER_FINDBYEMAIL_ERROR.description
            raise UserNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_FINDBYEMAIL_ERROR.phrase
            developer_message = "%s. Find by specified email return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYEMAIL_ERROR.description
            error_code = AuthError.USER_FINDBYEMAIL_ERROR.value
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)

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
            error_message = AuthError.USER_FINDALL_ERROR_DB.phrase
            error_code = AuthError.USER_FINDALL_ERROR_DB.value
            developer_message = "%s. DatabaseError. Something wrong with database or SQL is broken. " \
                                "Code: %s . %s" % (AuthError.USER_FINDALL_ERROR_DB.description, e.pgcode, e.pgerror)
            raise UserException(error=error_message, error_code=error_code, developer_message=developer_message)
        user_list = []

        for user_db in user_db_list:
            user = self.__map_userdb_to_user(user_db)
            user_list.append(user)

        if len(user_list) == 0:
            logging.warning('Empty User list of method find_all. Very strange behaviour.')

        return user_list

    def __map_userdb_to_user(self, user_db):
        self._uuid = user_db[self._uuid_field]
        return User(uuid=self._uuid,
                    email=user_db[self._email_field],
                    is_expired=user_db[self._is_expired_field],
                    is_locked=user_db[self._is_locked_field],
                    is_password_expired=user_db[self._is_password_expired_field],
                    created_date=user_db[self._created_date_field],
                    password=user_db[self._password_field],
                    enabled=user_db[self._enabled_field])
