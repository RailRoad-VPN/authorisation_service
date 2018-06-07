from enum import Enum

name = 'AUTH-'
i = 0


def count():
    global i
    i += 1
    return i


def get_all_error_codes():
    return [e.code for e in AuthError]


class AuthError(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, code, message, developer_message):
        self.code = code
        self.message = message
        self.developer_message = developer_message

    UNKNOWN_ERROR_CODE = (name + str(count()), 'UNKNOWN_ERROR_CODE phrase', 'UNKNOWN_ERROR_CODE description')

    USER_UPDATE_ERROR_DB = (name + str(count()), 'USER_UPDATE_ERROR_DB phrase', 'USER_UPDATE_ERROR_DB description')
    USER_FINDBYUUID_ERROR_DB = (name + str(count()), 'USER_FINDBYUUID_ERROR_DB phrase', 'USER_FINDBYUUID_ERROR_DB description')
    USER_FINDBYUUID_ERROR = (name + str(count()), 'USER_FINDBYUUID_ERROR phrase', 'USER_FINDBYUUID_ERROR description')
    USER_FINDBYEMAIL_ERROR_DB = (name + str(count()), 'USER_FINDBYEMAIL_ERROR_DB phrase', 'USER_FINDBYEMAIL_ERROR_DB description')
    USER_FINDBYEMAIL_ERROR = (name + str(count()), 'USER_FINDBYEMAIL_ERROR phrase', 'USER_FINDBYEMAIL_ERROR description')
    USER_FINDALL_ERROR_DB = (name + str(count()), 'USER_FINDALL_ERROR_DB phrase', 'USER_FINDALL_ERROR_DB description')
    USER_CREATE_ERROR_DB = (name + str(count()), 'USER_CREATE_ERROR_DB phrase', 'USER_CREATE_ERROR_DB description')


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
