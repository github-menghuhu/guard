from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from guard.core.config import DatabaseType, settings

if settings.DATABASE_TYPE == DatabaseType.POSTGRESQL:
    driver_name = "postgresql+asyncpg"
else:
    driver_name = "mysql+aiomysql"

url_object = URL.create(
    drivername=driver_name,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    database=settings.DATABASE_NAME,
)
print(f">>>>url_object:{url_object.render_as_string(hide_password=False)}")
engine = create_async_engine(url_object, echo=settings.IS_PRINT_SQL, future=True)
async_session_maker = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)
