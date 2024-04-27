from sqlalchemy.orm import Session

from models import User, Person

class UserRepository:
    @staticmethod
    def find_all(db: Session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def save(db: Session, user: User) -> User:
        if user.id:
            db.merge(user)
        else:
            db.add(user)
        db.commit()
        return user

    @staticmethod
    def find_by_id(db: Session, id: int) -> User:
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(User).filter(User.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        user = db.query(User).filter(User.id == id).first()
        if user is not None:
            db.delete(user)
            db.commit()


class PersonRepository:
    @staticmethod
    def find_all(db: Session) -> list[Person]:
        return db.query(Person).all()

    @staticmethod
    def save(db: Session, person: Person) -> Person:
        if person.id:
            db.merge(person)
        else:
            db.add(person)
        db.commit()
        return person

    @staticmethod
    def find_by_id(db: Session, id: int) -> Person:
        return db.query(Person).filter(Person.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Person).filter(Person.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        person = db.query(Person).filter(User.id == id).first()
        if person is not None:
            db.delete(person)
            db.commit()