import datetime
import logging
import sys
import uuid as uuidlib
from typing import List, Optional

from psycopg2._psycopg import DatabaseError

from app.exception import UserTicketException, AuthError, UserTicketNotFoundException

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserTicket(object):
    __version__ = 1

    logger = logging.getLogger(__name__)

    _suuid = None
    _number = None
    _user_uuid = None
    _contact_email = None
    _description = None
    _zip_path = None
    _status_id = None
    _extra_info = None
    _modify_reason = None
    _modify_date = None
    _created_date = None

    def __init__(self, suuid: str = None, number: int = None, user_uuid: str = None, contact_email: str = None,
                 description: str = None, zip_path: str = None, status_id: int = None, extra_info: dict = None,
                 modify_reason: str = None, modify_date: datetime = None,
                 created_date: datetime = None):
        self._suuid = suuid
        self._number = number
        self._user_uuid = user_uuid
        self._contact_email = contact_email
        self._description = description
        self._zip_path = zip_path
        self._status_id = status_id
        self._extra_info = extra_info
        self._modify_reason = modify_reason
        self._modify_date = modify_date
        self._created_date = created_date

    def to_dict(self):
        return {
            'uuid': str(self._suuid),
            'number': str(self._number),
            'user_uuid': str(self._user_uuid),
            'contact_email': self._contact_email,
            'description': self._description,
            'zip_path': self._zip_path,
            'status_id': self._status_id,
            'extra_info': self._extra_info,
            'modify_reason': self._modify_reason,
            'modify_date': self._modify_date,
            'created_date': self._created_date,
        }

    def to_api_dict(self):
        return self.to_dict()


class UserTicketStored(StoredObject, UserTicket):
    __version__ = 1

    logger = logging.getLogger(__name__)

    def __init__(self, storage_service: StorageService, suuid: str = None, number: int = None, user_uuid: str = None,
                 contact_email: str = None, description: str = None, zip_path: str = None, status_id: int = None,
                 extra_info: dict = None, modify_reason: str = None, created_date: datetime = None, limit: int = None,
                 offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserTicket.__init__(self, suuid=suuid, number=number, user_uuid=user_uuid, contact_email=contact_email,
                            description=description, zip_path=zip_path, status_id=status_id, extra_info=extra_info,
                            modify_reason=modify_reason, created_date=created_date)


class TicketDB(UserTicketStored):
    __version__ = 1

    logger = logging.getLogger(__name__)

    _suuid_field = 'uuid'
    _number_field = 'number'
    _user_uuid_field = 'user_uuid'
    _contact_email_field = 'contact_email'
    _description_field = 'description'
    _zip_path_field = 'zip_path'
    _status_id_field = 'status_id'
    _extra_info_field = 'extra_info'
    _modify_reason_field = 'modify_reason'
    _modify_date_field = 'modify_date'
    _created_date_field = 'created_date'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self) -> str:
        self._suuid = uuidlib.uuid4()
        self.logger.info('Create object UserTicket with uuid: ' + str(self._suuid))
        create_user_ticket_sql = '''
                          INSERT INTO public.ticket 
                            (
                                uuid,
                                user_uuid,
                                contact_email,
                                description,
                                zip_path,
                                status_id,
                                extra_info
                            ) 
                          VALUES 
                            (?, ?, ?, ?, ?, ?, ?)
                          RETURNING number;
        '''
        create_user_ticket_params = (
            self._suuid,
            self._user_uuid,
            self._contact_email,
            self._description,
            self._zip_path,
            self._status_id,
            self._extra_info,
        )
        self.logger.debug('Create UserTicket SQL : %s' % create_user_ticket_sql)

        try:
            self.logger.debug('Call database service')
            self._number = self._storage_service.create(sql=create_user_ticket_sql, data=create_user_ticket_params,
                                                        is_return=True)[0][self._number_field]
        except DatabaseError as e:
            self._storage_service.rollback()
            self.logger.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_TICKET_CREATE_ERROR_DB.message
            error_code = AuthError.USER_TICKET_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)
        self.logger.debug('UserTicket created.')

        return str(self._number)

    def set_zip_path(self, zip_path):
        self.logger.info('set_zip_path UserTicket')

        update_sql = '''
                    UPDATE public.ticket 
                    SET zip_path = ?
                    WHERE number = ?;
        '''

        self.logger.debug('Update SQL: %s' % update_sql)

        params = (
            zip_path,
            self._number,
        )
        try:
            self.logger.debug(f"{self.__class__}: Call database service")
            self._storage_service.update(update_sql, params)
        except DatabaseError as e:
            self._storage_service.rollback()
            self.logger.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_TICKET_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_TICKET_UPDATE_ERROR_DB.code
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

    def update(self):
        self.logger.info('Update UserTicket')

        update_sql = '''
                    UPDATE 
                      public.ticket 
                    SET 
                      user_uuid = ?,
                      contact_email = ?,
                      description = ?,
                      zip_path = ?,
                      status_id = ?,
                      modify_reason = ?
                    WHERE 
                      uuid = ?;
        '''

        self.logger.debug('Update SQL: %s' % update_sql)

        params = (
            self._user_uuid,
            self._contact_email,
            self._description,
            self._zip_path,
            self._status_id,
            self._modify_reason,
            self._suuid,
        )
        try:
            self.logger.debug(f"{self.__class__}: Call database service")
            self._storage_service.update(update_sql, params)
        except DatabaseError as e:
            self._storage_service.rollback()
            self.logger.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_TICKET_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_TICKET_UPDATE_ERROR_DB.code
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

    def delete(self):
        self.logger.info('delete UserTicket')

        delete_sql = '''
                      DELETE FROM public.ticket WHERE uuid = ?;
                     '''

        self.logger.debug('delete SQL: %s' % delete_sql)

        params = (self._suuid,)
        try:
            self.logger.debug(f"{self.__class__}: Call database service")
            self._storage_service.delete(sql=delete_sql, data=params)
        except DatabaseError as e:
            self._storage_service.rollback()
            self.logger.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_TICKET_DELETE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_DELETE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_TICKET_DELETE_ERROR_DB.code
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

    def find_by_suuid(self) -> Optional[UserTicket]:
        self.logger.info('Find UserTicket by uuid')
        select_sql = '''
                        SELECT 
                            uuid,
                            number,
                            user_uuid,
                            contact_email,
                            description,
                            zip_path,
                            status_id,
                            extra_info,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.ticket 
                        WHERE 
                            uuid = ?
                    '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            self.logger.debug('Call database service')
            user_ticket_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            self.logger.error(e)
            error_message = AuthError.USER_TICKET_FINDBYUUID_ERROR_DB.message
            error_code = AuthError.USER_TICKET_FINDBYUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_FINDBYUUID_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_ticket_list_db) == 1:
            user_ticket_db = user_ticket_list_db[0]
        elif len(user_ticket_list_db) == 0:
            error_message = AuthError.USER_TICKET_FINDBYUUID_ERROR.message
            error_code = AuthError.USER_TICKET_FINDBYUUID_ERROR.code
            developer_message = AuthError.USER_TICKET_FINDBYUUID_ERROR.developer_message
            raise UserTicketNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = AuthError.USER_TICKET_FINDBYUUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_FINDBYUUID_ERROR.developer_message
            error_code = AuthError.USER_TICKET_FINDBYUUID_ERROR.code
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_user_ticketdb_to_user_ticket(user_ticket_db=user_ticket_db)

    def find_by_ticket_number(self) -> Optional[UserTicket]:
        self.logger.info('Find UserTicket by number')
        select_sql = '''
                        SELECT 
                            uuid,
                            number,
                            user_uuid,
                            contact_email,
                            description,
                            zip_path,
                            status_id,
                            extra_info,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.ticket 
                        WHERE 
                            number = ?
                    '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._number,)

        try:
            self.logger.debug('Call database service')
            user_ticket_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            self.logger.error(e)
            error_message = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR_DB.message
            error_code = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_ticket_list_db) == 1:
            user_ticket_db = user_ticket_list_db[0]
        elif len(user_ticket_list_db) == 0:
            error_message = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.message
            error_code = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.code
            developer_message = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.developer_message
            raise UserTicketNotFoundException(error=error_message, error_code=error_code,
                                              developer_message=developer_message)
        else:
            error_message = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.message
            developer_message = "%s. Find by specified ticket number return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.developer_message
            error_code = AuthError.USER_TICKET_FINDBYTICKETNUMBER_ERROR.code
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_user_ticketdb_to_user_ticket(user_ticket_db=user_ticket_db)

    def find_by_user_uuid(self) -> List[UserTicket]:
        self.logger.info('Find UserTicket by ticket_token')
        select_sql = '''
                        SELECT 
                            uuid,
                            number,
                            user_uuid,
                            contact_email,
                            description,
                            zip_path,
                            status_id,
                            extra_info,
                            modify_reason,
                            to_json(modify_date) AS modify_date,
                            to_json(created_date) AS created_date
                        FROM 
                            public.ticket 
                        WHERE 
                            user_uuid = ?
                    '''
        self.logger.debug(f"{self.__class__}: Select SQL: {select_sql}")
        params = (self._user_uuid,)

        try:
            self.logger.debug('Call database service')
            user_ticket_list_db = self._storage_service.get(select_sql, params)
        except DatabaseError as e:
            self.logger.error(e)
            error_message = AuthError.USER_TICKET_FINDBYUSERUUID_ERROR_DB.message
            error_code = AuthError.USER_TICKET_FINDBYUSERUUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_TICKET_FINDBYUSERUUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserTicketException(error=error_message, error_code=error_code, developer_message=developer_message)

        user_ticket_list = []
        for user_ticket_db in user_ticket_list_db:
            user_ticket = self.__map_user_ticketdb_to_user_ticket(user_ticket_db=user_ticket_db)
            user_ticket_list.append(user_ticket)

        return user_ticket_list

    def __map_user_ticketdb_to_user_ticket(self, user_ticket_db):
        return UserTicket(suuid=user_ticket_db[self._suuid_field],
                          number=user_ticket_db[self._number_field],
                          user_uuid=user_ticket_db[self._user_uuid_field],
                          contact_email=user_ticket_db[self._contact_email_field],
                          description=user_ticket_db[self._description_field],
                          zip_path=user_ticket_db[self._zip_path_field],
                          status_id=user_ticket_db[self._status_id_field],
                          extra_info=user_ticket_db[self._extra_info_field],
                          modify_reason=user_ticket_db[self._modify_reason_field],
                          modify_date=user_ticket_db[self._modify_date_field],
                          created_date=user_ticket_db[self._created_date_field])
