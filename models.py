from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase
from database import Base

class Person(Base):
    __tablename__ = 'persons'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    users = relationship("User", back_populates="person")



class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"))
    person = relationship("Person", back_populates="user")

    __table_args__ = (UniqueConstraint("person_id"),)
