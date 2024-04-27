from repositories import PersonRepository, UserRepository
from schemas import UserCreate, PersonCreate
from database import get_db


class PersonService:
    repository = PersonRepository
    schema_create = UserCreate
    schema_update = None
    schema_list = None


    @classmethod
    async def create(cls, data):
        object_data = cls.schema_create(**data)

        object = await cls.repository.create(object_data.model_dump(), db=db, commit=commit)
        return object


class UserService:
    repository = UserRepository
    schema_create = PersonCreate
    schema_update = None
    schema_list = None


    @classmethod
    async def create(cls, data):
        object_data = cls.schema_create(**data)

        object = await cls.repository.create(object_data.model_dump(), db=db, commit=commit)
        return object
