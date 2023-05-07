"""
License Goes Here
"""

from typing import Optional, List

from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from random import randint

from . import Base, engine

from api.models.flag import IntermediaryFlag

class FlagDb(Base):
    """
    Flag DB
    =======
    Controls applications interaction with flag database
    """
    
    __tablename__ = "flags"

    id = Column('flagid', String, primary_key=True)
    budget_id = Column('budgetid', String, nullable=False)
    display_name = Column('displayname', String, nullable=False)
    user_id = Column('userid', String, nullable=False)
    
    @staticmethod
    def add_flag(db: Session, flag: IntermediaryFlag) -> 'FlagDb':
        
        db_flag = FlagDb(
            id=FlagDb.generate_id(db),
            display_name=flag.display_name,
            budget_id=flag.budget_id,
            user_id=flag.user_id
        )
        db.add(db_flag)
        db.commit()
        db.refresh(db_flag)
        return db_flag
    
    @staticmethod
    def generate_id(db: Session) -> str:
        """Generates a globally unique alphanumerical category id.

        Args:
            db (Session): Database session

        Returns:
            str: A globally unique alphanumerical category id
        """
        
        # self.logger.debug('Generating an account ID')
        flag_id = None

        while flag_id is None:
            flag_id = str(randint(1e9, (1e10 - 1)))

            result = db.query(FlagDb).filter(FlagDb.id == flag_id).first()

            if result is not None:
                flag_id = None

        return flag_id
    
    @staticmethod
    def list_flags(db: Session, budget_id: str) -> List['FlagDb']:
        """Lists flags for budget_id

        Returns:
            List[FlagDb]: List of flags
        """
    
        return db.query(FlagDb).filter(FlagDb.budget_id == budget_id).all()
    
    @staticmethod
    def get_flag(db: Session, flag_id: str) -> Optional['FlagDb']:
        """Gets the flag based off id

        Returns:
            Optional[FlagDb]: The flag
        """
        
        return db.query(FlagDb).filter(FlagDb.id == flag_id).first()
    
    
FlagDb.__table__.create(bind=engine, checkfirst=True)