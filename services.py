from repositories import PersonRepository, UserRepository
from schemas import UserCreate, PersonCreate, InitialPersonCreate
from database import get_db
from models import User, Person


class PersonService:
    repository = PersonRepository
    schema_create = PersonCreate
    schema_update = None
    schema_list = None


    @classmethod
    async def create(cls, data):
        object_data = cls.schema_create(**data)

        object = await cls.repository.create(object_data.model_dump(), db=db, commit=commit)
        return object


class UserService:
    repository = UserRepository
    schema_create = InitialPersonCreate
    schema_update = None
    schema_list = None


    # @classmethod
    # async def create(cls, data):
    #     object_data = cls.schema_create(**data)
        
    #     db = get_db()

    #     person = Person

    #     object = await UserRepository.save(db=db, object_data.model_dump())
    #     return object


class InitialPersonService:


    @classmethod
    async def create(cls, data: InitialPersonCreate):
        object_data = data.model_dump()

        db = get_db()

        person = Person(
            email=object_data["email"],
            first_name=object_data["first_name"],
            last_name=object_data["last_name"]
        )

        person = await PersonRepository.save(db=db, person=person)

        # user = User(
        #     username=object_data["username"],
        #     email=object_data["email"],
        #     first_name=object_data["first_name"],
        #     last_name=object_data["last_name"],
        #     person=person
        # )

        # user = await UserRepository.save(db=db, user=user)

        
        return person
