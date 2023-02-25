import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, LargeBinary, and_
import random
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

class CategoryDb:
    """
    CategoryDb provides a set of helper functions over SQLAlchemy
    to handle db operations for userservice
    """

    def __init__(self, uri, logger=logging):
        self.engine = create_engine(uri)
        self.logger = logger
        self.categories_table = Table(
            'categories',
            MetaData(self.engine),
            Column('categoryid', String, primary_key=True),
            Column('displayname', String, nullable=False),
            Column('parentid', String, nullable=True),
            Column('budgetid', String, nullable=False),
        )
        # Set up tracing autoinstrumentation for sqlalchemy
        SQLAlchemyInstrumentor().instrument(
            engine=self.engine,
            service='categories',
        )
    
    def add_category(self, category):
        """Add a budget to the database.
        Params: budget - a key/value dict of attributes describing a new budget
                    {'email': email, 'password': password, ...}
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.categories_table.insert().values(category)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            conn.execute(statement)

    def generate_categoryid(self):
        """Generates a globally unique alphanumerical budgetid."""
        self.logger.debug('Generating an account ID')
        categoryid = None
        with self.engine.connect() as conn:
            while categoryid is None:
                categoryid = str(random.randint(1e9, (1e10 - 1)))

                statement = self.categories_table.select().where(
                    self.categories_table.c.categoryid == categoryid
                )
                self.logger.debug('QUERY: %s', str(statement))
                result = conn.execute(statement).first()
                # If there already exists an account, try again.
                if result is not None:
                    categoryid = None
                    self.logger.debug(
                        'RESULT: account ID already exists. Trying again')
        self.logger.debug('RESULT: account ID generated.')
        return categoryid

    def get_category(self, categoryid):
        """Get user data for the specified email.
        Params: email - the email of the user
        Return: a key/value dict of user attributes,
                {'email': email, 'userid': userid, ...}
                or None if that user does not exist
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.categories_table.select().where(
            self.categories_table.c.categoryid == categoryid)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            result = conn.execute(statement).first()
        self.logger.debug('RESULT: fetched budget data for %s', categoryid)
        return dict(result) if result is not None else None
    
    def get_categories(self, budgetid):
        statement = self.categories_table.select().where(and_(self.categories_table.c.budgetid == budgetid,self.categories_table.c.parentid == None))
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            results = conn.execute(statement)
        self.logger.debug('RESULT: fetched categories for budgetid %s', budgetid)
        return [dict(result) for result in results] if results is not None else None

    def delete_category(self, categoryid):
        """_summary_

        Args:
            budgetid (_type_): _description_
        """
        statement = self.budgets_table.delete().where(
            self.categories_table.c.categoryid == categoryid)
        with self.engine.connect() as conn:
            results = conn.execute(statement)

        self.logger.debug('QUERY: %s', str(statement))
        return {}
    
    def update_category(self, category: dict):

        statement = self.budgets_table.update().values(category).where(
            self.categories_table.c.budgetid == category["budgetid"])
        with self.engine.connect() as conn:
            results = conn.execute(statement)
