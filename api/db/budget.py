"""
License Goes Here
"""

from typing import Optional, List

from sqlalchemy import Column, String, Date
from sqlalchemy.orm import Session

from random import randint

from . import Base, engine

from api.models.budget import Budget


class BudgetDb(Base):

    __tablename__ = "budgets"

    id = Column('budgetid', String, primary_key=True)
    display_name = Column('displayname', String, nullable=False)
    notes = Column('budgetnotes', String, nullable=True)
    accessed_date = Column('accessdate', Date, nullable=False)
    user_id = Column('userid', String, nullable=False)
    
    @staticmethod
    def add_budget(db: Session, budget: Budget) -> 'BudgetDb':
        
        db_budget = BudgetDb(
            id=BudgetDb.generate_id(db),
            display_name=budget.display_name,
            notes=budget.notes,
            accessed_date=budget.accessed_date,
            user_id=budget.user_id
        )
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget
    
    @staticmethod
    def generate_id(db: Session) -> str:
        """Generates a globally unique alphanumerical budget id.

        Args:
            db (Session): Database session

        Returns:
            str: A globally unique alphanumerical budget id
        """

        # self.logger.debug('Generating an account ID')
        budget_id = None

        while budget_id is None:
            budget_id = str(randint(1e9, (1e10 - 1)))

            result = db.query(BudgetDb).filter(BudgetDb.id == budget_id).first()

            if result is not None:
                budget_id = None

        return budget_id
    
    @staticmethod
    def list_budgets(db: Session, user_id: str) -> List['BudgetDb']:
    
        return db.query(BudgetDb).filter(BudgetDb.user_id == user_id).all()
    
    @staticmethod
    def get_budget(db: Session, budget_id: str) -> Optional['BudgetDb']:
        
        return db.query(BudgetDb).filter(BudgetDb.id == budget_id).first()
    
    @staticmethod
    def delete_budget(db: Session, budget_id: str):
        
        db_budget = BudgetDb.get_budget(db, budget_id)
        
        db.delete(db_budget)
        
        db.commit()
        db.refresh(db_budget)
        
        return None
    
    @staticmethod
    def update_budget(db: Session, budget: Budget):
        pass
    
BudgetDb.__table__.create(bind=engine, checkfirst=True)