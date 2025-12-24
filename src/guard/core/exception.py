from api_exception import BaseExceptionCode


class CustomExceptionCode(BaseExceptionCode):
    """
    数据库错误
    """

    # 连接超时
    DB_CONNECTION_TIMEOUT = (
        "DB-001",
        "Database Connection Timeout.",
        "Database connection timed out. Please check network connectivity and database status.",
    )
