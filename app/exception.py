from enum import IntEnum


class AuthError(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    UNKNOWN_ERROR_CODE = (0, 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    USER_UPDATE_ERROR_DB = (1, 'USER_UPDATE_ERROR_DB phrase', 'USER_UPDATE_ERROR_DB description')
    USER_FINDBYUUID_ERROR_DB = (2, 'USER_FINDBYUUID_ERROR_DB phrase', 'USER_FINDBYUUID_ERROR_DB description')
    USER_FINDBYUUID_ERROR = (3, 'USER_FINDBYUUID_ERROR phrase', 'USER_FINDBYUUID_ERROR description')
    USER_FINDBYEMAIL_ERROR_DB = (4, 'USER_FINDBYEMAIL_ERROR_DB phrase', 'USER_FINDBYEMAIL_ERROR_DB description')
    USER_FINDBYEMAIL_ERROR = (5, 'USER_FINDBYEMAIL_ERROR phrase', 'USER_FINDBYEMAIL_ERROR description')
    USER_FINDALL_ERROR_DB = (6, 'USER_FINDALL_ERROR_DB phrase', 'USER_FINDALL_ERROR_DB description')
    USER_CREATE_ERROR_DB = (7, 'USER_CREATE_ERROR_DB phrase', 'USER_CREATE_ERROR_DB description')


class AuthException(Exception):
    __version__ = 1

    error = None
    error_code = None
    developer_message = None

    def __init__(self, error: str, error_code: int, developer_message: str = None, *args):
        super().__init__(*args)
        self.error = error
        self.error_code = error_code
        self.developer_message = developer_message


class UserException(AuthException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserNotFoundException(AuthException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)