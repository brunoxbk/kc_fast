from invoke import task


@task
def run(c):
    c.run("uvicorn main:app --reload --host 0.0.0.0 --port 80")


@task
def init_migrations(c):
    c.run("alembic init migrations")


@task
def mkmigration(c, name_table):
    c.run(f'''alembic revision --autogenerate -m "create {name_table} table"''')


@task
def migrate(c):
    c.run("alembic upgrade head")
