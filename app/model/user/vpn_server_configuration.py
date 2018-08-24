import logging
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class UserVPNServerConfiguration(object):
    __version__ = 1

    _suuid = None
    _user_uuid = None
    _vpn_device_platform_id = None
    _vpn_type_id = None
    _configuration = None
    _version = None

    def __init__(self, suuid: str = None, user_uuid: str = None, vpn_device_platform_id: int = None,
                 vpn_type_id: int = None, configuration: str = None, version: int = None):
        self._suuid = suuid
        self._user_uuid = user_uuid
        self._vpn_device_platform_id = vpn_device_platform_id
        self._vpn_type_id = vpn_type_id
        self._configuration = configuration
        self._version = version

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'user_uuid': self._user_uuid,
            'vpn_type_id': self._vpn_type_id,
            'vpn_device_platform_id': self._vpn_device_platform_id,
            'configuration': self._configuration,
            'version': self._version,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'user_uuid': str(self._user_uuid),
            'vpn_type_id': self._vpn_type_id,
            'vpn_device_platform_id': self._vpn_device_platform_id,
            'configuration': self._configuration,
            'version': self._version,
        }


class UserVPNServerConfigurationStored(StoredObject, UserVPNServerConfiguration):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, user_uuid: str = None,
                 vpn_device_platform_id: int = None, vpn_type_id: int = None, configuration: str = None,
                 version: int = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        UserVPNServerConfiguration.__init__(self, suuid=suuid, user_uuid=user_uuid, vpn_type_id=vpn_type_id,
                                            vpn_device_platform_id=vpn_device_platform_id, configuration=configuration,
                                            version=version)


class UserVPNServerConfigurationDB(UserVPNServerConfigurationStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _user_uuid_field = 'user_uuid'
    _vpn_device_platform_id_field = 'vpn_device_platform_id'
    _vpn_type_id_field = 'vpn_type_id'
    _configuration_field = 'configuration'
    _version_field = 'version'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        self.logger.info('UserVPNServerConfigurationDB find method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        vpn_device_platform_id,
                        vpn_type_id,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.user_vpn_server_config
                      '''
        if self._limit:
            select_sql += f"\nLIMIT {self._limit}\nOFFSET {self._offset}"
        self.logger.debug(f"Select SQL: {select_sql}")

        try:
            self.logger.debug('Call database service')
            vpnserverconfig_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_ERROR_DB.message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_VPNSERVERCONFIG_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconfig_list = []

        for vpnserverconfig_db in vpnserverconfig_list_db:
            vpnserverconfig = self.__map_uservpnserverconfigdb_to_uservpnserverconfig(vpnserverconfig_db)
            vpnserverconfig_list.append(vpnserverconfig)

        return vpnserverconfig_list

    def find_by_suuid(self):
        self.logger.info('UserVPNServerConfigurationDB find_by_suuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        vpn_device_platform_id,
                        vpn_type_id,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.user_vpn_server_config
                      WHERE uuid = ?
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            self.logger.debug('Call database service')
            user_vpn_server_config_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_vpn_server_config_list_db) == 1:
            vpnserver_db = user_vpn_server_config_list_db[0]
        elif len(user_vpn_server_config_list_db) == 0:
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.code
            developer_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.developer_message
            raise UserVPNServerConfigNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.developer_message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_UUID_ERROR.code
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_uservpnserverconfigdb_to_uservpnserverconfig(vpnserver_db)

    def find_by_user_platform_type(self):
        self.logger.info('UserVPNServerConfigurationDB find_by_user_platform_type method')
        select_sql = '''
                      SELECT 
                        uuid,
                        user_uuid,
                        vpn_device_platform_id,
                        vpn_type_id,
                        configuration,
                        version,
                        to_json(created_date) AS created_date 
                      FROM public.user_vpn_server_config
                      WHERE user_uuid = ? AND vpn_device_platform_id = ? AND vpn_type_id = ?
                      '''
        self.logger.debug(f"Select SQL: {select_sql}")
        params = (
            self._user_uuid,
            self._vpn_device_platform_id,
            self._vpn_type_id,
        )

        try:
            self.logger.debug('Call database service')
            user_vpn_server_config_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB.message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB.code
            developer_message = "%s. DatabaseError. Code: %s . %s" % (
                AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR_DB.developer_message, e.pgcode,
                e.pgerror
            )
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(user_vpn_server_config_list_db) == 1:
            user_vpn_server_config = user_vpn_server_config_list_db[0]
        elif len(user_vpn_server_config_list_db) == 0:
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.code
            developer_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.developer_message
            raise UserVPNServerConfigNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.developer_message
            error_code = AuthError.USER_VPNSERVERCONFIG_FIND_BY_USER_PLATFORM_TYPE_ERROR.code
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_uservpnserverconfigdb_to_uservpnserverconfig(user_vpn_server_config)

    def create(self):
        self.logger.info('UserVPNServerConfigurationDB create method')
        self._suuid = uuid.uuid4()
        self.logger.info('Create object UserVPNServerConfiguration with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.user_vpn_server_config 
                        (uuid, vpn_type_id, vpn_device_platform_id, user_uuid, configuration) 
                      VALUES 
                        (?, ?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._vpn_type_id,
            self._vpn_device_platform_id,
            self._user_uuid,
            self._configuration,
        )
        self.logger.debug('Create SQL : %s' % insert_sql)

        try:
            self.logger.debug('Call database service')
            self._storage_service.create(sql=insert_sql, data=insert_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_VPNSERVER_CREATE_ERROR_DB.message
            error_code = AuthError.USER_VPNSERVER_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.VPNSERVERCONFIG_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)
        self.logger.debug('UserVPNServerConfiguration created.')

        return self._suuid

    def update(self):
        self.logger.info('UserVPNServerConfigurationDB update method')

        update_sql = '''
                    UPDATE public.user_vpn_server_config 
                    SET
                        user_uuid = ?,  
                        vpn_type_id = ?, 
                        vpn_device_platform_id = ?, 
                        configuration = ?,
                        version = version + 1
                    WHERE 
                      uuid = ?
                    '''

        self.logger.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._vpn_type_id,
            self._vpn_device_platform_id,
            self._user_uuid,
            self._configuration,
            self._suuid,
        )

        try:
            self.logger.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            self.logger.debug('VPNServerConfiguration updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = AuthError.USER_VPNSERVERCONFIG_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    AuthError.USER_VPNSERVERCONFIG_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = AuthError.USER_VPNSERVERCONFIG_UPDATE_ERROR_DB.code
            raise UserVPNServerConfigException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_uservpnserverconfigdb_to_uservpnserverconfig(self, vpnserverconfig_db):
        return UserVPNServerConfiguration(
            suuid=vpnserverconfig_db[self._suuid_field],
            user_uuid=vpnserverconfig_db[self._user_uuid_field],
            vpn_type_id=vpnserverconfig_db[self._vpn_type_id_field],
            vpn_device_platform_id=vpnserverconfig_db[self._vpn_device_platform_id_field],
            configuration=vpnserverconfig_db[self._configuration_field],
            version=vpnserverconfig_db[self._version_field],
        )
