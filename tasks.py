from invoke import task


@task
def run(c):
    c.run("poetry run uvicorn main:app --reload --host 0.0.0.0 --port 80")


@task
def init_migrations(c):
    c.run("poetry run alembic init migrations")


@task
def mkmigration(c, name_table):
    c.run(f'''poetry run alembic revision --autogenerate -m "create {name_table} table"''')


@task
def migrate(c):
    c.run("poetry run alembic upgrade head")
