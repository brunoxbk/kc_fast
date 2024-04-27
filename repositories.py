from sqlalchemy.orm import Session

from models import User, Person

class UserRepository:
    @staticmethod
    def find_all(db: Session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def save(db: Session, curso: User) -> User:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso

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
    def save(db: Session, curso: Person) -> Person:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso

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