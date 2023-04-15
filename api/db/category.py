"""
License Goes Here
"""

from typing import Optional, List

from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from random import randint

from . import Base, engine

from api.models.category import IntermediaryCategory

class CategoryDb(Base):

    __tablename__ = "categories"

    id = Column('categoryid', String, primary_key=True)
    budget_id = Column('budgetid', String, nullable=False)
    display_name = Column('displayname', String, nullable=False)
    user_id = Column('userid', String, nullable=False)
    
    @staticmethod
    def add_category(db: Session, category: IntermediaryCategory) -> 'CategoryDb':
        
        db_category = CategoryDb(
            id=CategoryDb.generate_id(db),
            display_name=category.display_name,
            budget_id=category.budget_id,
            user_id=category.user_id
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def generate_id(db: Session) -> str:
        """Generates a globally unique alphanumerical category id.

        Args:
            db (Session): Database session

        Returns:
            str: A globally unique alphanumerical category id
        """

        # self.logger.debug('Generating an account ID')
        category_id = None

        while category_id is None:
            category_id = str(randint(1e9, (1e10 - 1)))

            result = db.query(CategoryDb).filter(CategoryDb.id == category_id).first()

            if result is not None:
                category_id = None

        return category_id
    
    @staticmethod
    def list_categories(db: Session, budget_id: str) -> List['CategoryDb']:
    
        return db.query(CategoryDb).filter(CategoryDb.budget_id == budget_id).all()
    
    @staticmethod
    def get_category(db: Session, category_id: str) -> Optional['CategoryDb']:
        
        return db.query(CategoryDb).filter(CategoryDb.id == category_id).first()
    
CategoryDb.__table__.create(bind=engine, checkfirst=True)