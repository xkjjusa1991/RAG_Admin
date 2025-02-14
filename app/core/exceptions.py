from fastapi import HTTPException

class APIException(HTTPException):
    def __init__(
        self,
        code: int = 400,
        msg: str = "Bad request",
        status_code: int = 400,
        headers: dict = None
    ):
        self.code = code
        self.msg = msg
        super().__init__(status_code=status_code, headers=headers)


class AuthFailedException(APIException):
    def __init__(self, msg: str = "Authentication failed"):
        super().__init__(code=401, msg=msg, status_code=401)


class PermissionDeniedException(APIException):
    def __init__(self, msg: str = "Permission denied"):
        super().__init__(code=403, msg=msg, status_code=403)


class NotFoundException(APIException):
    def __init__(self, msg: str = "Resource not found"):
        super().__init__(code=404, msg=msg, status_code=404)


class ValidationException(APIException):
    def __init__(self, msg: str = "Validation error"):
        super().__init__(code=422, msg=msg, status_code=422) 