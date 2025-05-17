from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Ganti nilai-nilai ini sesuai dengan konfigurasi MySQL
DB_USER = "root"            # atau user lain dari phpMyAdmin
DB_PASSWORD = ""    # ganti dengan password MySQL
DB_HOST = "localhost"       # jika lokal
DB_PORT = "3306"
DB_NAME = "db_tugasmdik"   # ganti dengan nama database 

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Membuat engine asinkron
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency untuk inject session ke endpoint
async def get_db():
    async with async_session() as session:
        yield session
