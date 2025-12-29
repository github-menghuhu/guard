from api_exception import BaseExceptionCode


class ExceptionCode(BaseExceptionCode):
    # 请求错误 http 400
    BAD_REQUEST = (
        "BAD-001",
        "Bad Request.",
        "Your request is invalid or malformed.",
    )

    # 认证错误 http 401
    UNAUTHORIZED = (
        "AUTH-001",
        "Unauthorized.",
        "Authentication credentials were missing or invalid.",
    )

    # 权限错误 http 403
    FORBIDDEN = (
        "PERM-001",
        "Forbidden.",
        "You do not have permission to access this resource.",
    )

    # 没找到错误 http 404
    NOT_FOUND = (
        "RES-001",
        "Not Found.",
        "The requested resource could not be found.",
    )

    # 输入验证错误 http 422
    VALIDATION_ERROR = (
        "VAL-001",
        "Validation Error.",
        "Input validation failed.",
    )

    # 服务器错误 http 500
    INTERNAL_SERVER_ERROR = (
        "INT-001",
        "Internal Server Error.",
        "An unexpected error occurred on the server.",
    )

    # 数据库连接超时 http 500
    DB_CONNECTION_TIMEOUT = (
        "DB-001",
        "Database Connection Timeout.",
        "Database connection timed out. Please check network connectivity and database status.",
    )
