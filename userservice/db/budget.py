from logging import Logger
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, LargeBinary, and_
import random
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

class BudgetDb:
    """
    BudgetDb provides a set of helper functions over SQLAlchemy
    to handle db operations for userservice
    """

    def __init__(self, uri, logger: Logger):
        self.engine = create_engine(uri)
        self.logger = logger
        self.budgets_table = Table(
            'budgets',
            MetaData(self.engine),
            Column('budgetid', String, primary_key=True),
            Column('displayname', String, nullable=False),
            Column('budgetnotes', String, nullable=True),
            Column('accessdate', Date, nullable=False),
            Column('userid', String, nullable=False),
        )

        # Set up tracing autoinstrumentation for sqlalchemy
        SQLAlchemyInstrumentor().instrument(
            engine=self.engine,
            service='budgets',
        )
    
    def add_budget(self, budget):
        """Add a budget to the database.
        Params: budget - a key/value dict of attributes describing a new budget
                    {'email': email, 'password': password, ...}
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.budgets_table.insert().values(budget)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            conn.execute(statement)

    def generate_budgetid(self):
        """Generates a globally unique alphanumerical budgetid."""
        self.logger.debug('Generating an account ID')
        budgetid = None
        with self.engine.connect() as conn:
            while budgetid is None:
                budgetid = str(random.randint(1e9, (1e10 - 1)))

                statement = self.budgets_table.select().where(
                    self.budgets_table.c.budgetid == budgetid
                )
                self.logger.debug('QUERY: %s', str(statement))
                result = conn.execute(statement).first()
                # If there already exists an account, try again.
                if result is not None:
                    budgetid = None
                    self.logger.debug(
                        'RESULT: account ID already exists. Trying again')
        self.logger.debug('RESULT: account ID generated.')
        return budgetid

    def get_budget(self, budgetid):
        """Get user data for the specified email.
        Params: email - the email of the user
        Return: a key/value dict of user attributes,
                {'email': email, 'userid': userid, ...}
                or None if that user does not exist
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.budgets_table.select().where(
            self.budgets_table.c.budgetid == budgetid)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            result = conn.execute(statement).first()
        self.logger.debug('RESULT: fetched budget data for %s', budgetid)
        return dict(result) if result is not None else None
    
    def get_budgets(self, userid):
        statement = self.budgets_table.select().where(
            self.budgets_table.c.userid == userid)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            results = conn.execute(statement)
        self.logger.debug('RESULT: fetched budgets data for %s', userid)
        return [dict(result) for result in results] if results is not None else None

    def delete_budget(self, budgetid):
        """_summary_

        Args:
            budgetid (_type_): _description_
        """
        statement = self.budgets_table.delete().where(
            self.budgets_table.c.budgetid == budgetid)
        with self.engine.connect() as conn:
            results = conn.execute(statement)

        self.logger.debug('QUERY: %s', str(statement))
        return {}
    
    def update_budget(self, budget: dict):

        statement = self.budgets_table.update().values(budget).where(
            self.budgets_table.c.budgetid == budget["budgetid"])
        with self.engine.connect() as conn:
            results = conn.execute(statement)
