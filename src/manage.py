import typer
import asyncio
from config.db import engine
from models.models import Base

cli = typer.Typer()


async def async_migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")


@cli.command()
def migrate():
    asyncio.run(async_migrate())


if __name__ == "__main__":
    migrate()  # <-- This must be cli(), not migrate() or anything else
