# manage.py
import typer
import asyncio
from config.db import engine  # must be an AsyncEngine
from models.models import Base

cli = typer.Typer()


async def async_migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")


@cli.command("migrate")
def migrate():
    asyncio.run(async_migrate())


@cli.command("test")
def test():
    print("tested")


if __name__ == "__main__":
    cli()
