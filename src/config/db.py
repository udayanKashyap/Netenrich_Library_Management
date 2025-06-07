from click import echo
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# The DATABASE URL is not created as an env variable as i am using a cloud database (aiven.io)
# the database will already be popluated on submission.
DATABASE_URL = "postgresql+asyncpg://avnadmin:AVNS_gEF1ElbZ6XMfjZApNkq@netenrich-pharmafind.f.aivencloud.com:19072/defaultdb"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
