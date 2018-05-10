import sys

sys.path.insert(0, '../rest_api_library')
from exception import APIException


class AuthError(object):
    UNKNOWN_ERROR_CODE = 'AUTH-000000'

    USER_UPDATE_ERROR_DB = 'AUTH-00001'
    USER_FINDBYUUID_ERROR_DB = 'AUTH-00002'
    USER_FINDBYUUID_ERROR = 'AUTH-00003'
    USER_FINDBYEMAIL_ERROR_DB = 'AUTH-00004'
    USER_FINDBYEMAIL_ERROR = 'AUTH-00005'
    USER_FINDALL_ERROR_DB = 'AUTH-00007'
    USER_CREATE_ERROR_DB = 'AUTH-00008'


class UserException(APIException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserNotFoundException(APIException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
