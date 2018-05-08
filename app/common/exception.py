class AuthError(object):
    UNKNOWN_ERROR_CODE = 'AUTH-000000'

    USER_UPDATE_ERROR_DB = 'AUTH-00001'
    USER_FINDBYUUID_ERROR_DB = 'AUTH-00002'
    USER_FINDBYUUID_ERROR = 'AUTH-00003'
    USER_FINDBYEMAIL_ERROR_DB = 'AUTH-00004'
    USER_FINDBYEMAIL_ERROR = 'AUTH-00005'
    USER_FINDALL_ERROR_DB = 'AUTH-00007'
    USER_CREATE_ERROR_DB = 'AUTH-00008'


class AuthException(Exception):
    __version__ = 1

    code = None
    message = None
    data = None

    def __init__(self, message: str, code: int, data: dict = None, *args, **kwargs):
        super().__init__(*args)

        self.code = code
        self.message = message
        self.data = data


class APIException(AuthException):
    __version__ = 1

    http_code = None

    def __init__(self, message: str, code: int, http_code: int, data: dict = None, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)

        self.http_code = http_code
        self.data = data


class UserException(AuthException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserNotFoundException(UserException):
    __version__ = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
