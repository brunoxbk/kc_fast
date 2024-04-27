from pydantic import BaseModel, ConfigDict, EmailStr, UUID4


class PersonCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    email: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    person_id: str



class InitialPersonCreate(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    phone: str
    username: str
    password: str
    email: EmailStr
    zip_code: str
    address: str
    complement: str
    city_id: UUID4


class InitialPersonRetrieve(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr