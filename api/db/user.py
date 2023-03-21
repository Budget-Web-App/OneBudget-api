from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary, Date
from sqlalchemy.orm import relationship, Session

from random import randint

from . import Base, engine

from api.models.user import User


class UserDb(Base):

    __tablename__ = "users"

    id = Column('userid', String, primary_key=True)
    email = Column('email', String, unique=True, nullable=False)
    pass_hash = Column('passhash', LargeBinary, nullable=False)
    timezone = Column('timezone', String, nullable=True)
    registered_date = Column('registereddate', Date, nullable=True)

    @staticmethod
    def add_user(db: Session, user: User) -> 'UserDb':
        """Adds user to database

        Args:
            db (Session): The database session
            user (User): The user to add

        Returns:
            UserDb: The newly created user
        """
        
        existing_user = UserDb.get_user(db, user.email)
        
        if existing_user is not None:
            raise Exception(f"User with email {user.email} already exists")

        db_user = UserDb(
            id=UserDb.generate_userid(db),
            email=user.email,
            pass_hash=user.pass_hash,
            registered_date=user.registered_date
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def generate_userid(db: Session) -> str:
        """Generates a globally unique alphanumerical userid.

        Args:
            db (Session): Database session

        Returns:
            str: A globally unique alphanumerical userid
        """

        # self.logger.debug('Generating an account ID')
        userid = None

        while userid is None:
            userid = str(randint(1e9, (1e10 - 1)))

            result = db.query(UserDb).filter(UserDb.id == userid).first()

            if result is not None:
                userid = None

        return userid

    @staticmethod
    def get_user(db: Session, email: str) -> Optional['UserDb']:
        """Gets the user with the provided email
        
        Args:
            db (Session): Database session
            email (str): The email to query by

        Returns:
            Optional[UserDb]: The user with the provided email
        """
        
        return db.query(UserDb).filter(UserDb.email == email).first()
    
UserDb.__table__.create(bind=engine, checkfirst=True)