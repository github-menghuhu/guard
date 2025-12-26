from api_exception import BaseExceptionCode


class ExceptionCode(BaseExceptionCode):
    """
    数据库错误
    """

    # 连接超时
    DB_CONNECTION_TIMEOUT = (
        "DB-001",
        "Database Connection Timeout.",
        "Database connection timed out. Please check network connectivity and database status.",
    )

    """
    校验错误
    """

    # 资源不存在
    RESOURCE_NOT_FOUND = (
        "RES-001",
        "Resource Not Found.",
        "The requested resource does not exist.",
    )
