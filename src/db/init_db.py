from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://src/db/db.sqlite3',
        modules={'models': ['src.users.models']}
    )
    await Tortoise.generate_schemas()
