import os

from alembic.command import upgrade
from alembic.config import Config


def run_sql_migrations():
    # retrieves the directory that *this* file is in
    migrations_dir = os.path.dirname(os.path.realpath(__file__))
    # this assumes the alembic.ini is also contained in this same directory
    config_file = os.path.join(migrations_dir, "alembic.ini")

    config = Config(file_=config_file)
    config.set_main_option("script_location", migrations_dir)

    # upgrade the database to the latest revision
    upgrade(config, "head")
