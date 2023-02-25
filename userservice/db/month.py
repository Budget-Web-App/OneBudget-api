import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, LargeBinary, and_
import random
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


class MonthDb:
    """
    MonthDb provides a set of helper functions over SQLAlchemy
    to handle db operations for userservice
    """

    def __init__(self, uri, logger=logging):
        self.engine = create_engine(uri)
        self.logger = logger
        self.months_table = Table(
            'months',
            MetaData(self.engine),
            Column('monthid', String, primary_key=True),
            Column('budgetid', String, nullable=False),
            Column('month', String, nullable=False),
            Column('note', String, nullable=True),
            Column('income', String, nullable=True),
            Column('budgeted', String, nullable=True),
            Column('activity', String, nullable=True),
            Column('to_be_budgeted', String, nullable=True),
            Column('age_of_money', String, nullable=True),
        )

        # Set up tracing autoinstrumentation for sqlalchemy
        SQLAlchemyInstrumentor().instrument(
            engine=self.engine,
            service='months',
        )
    
    def add_month(self, month):
        """Add a month to the database.
        Params: budget - a key/value dict of attributes describing a new month
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.months_table.insert().values(month)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            conn.execute(statement)

    def generate_monthid(self):
        """Generates a globally unique alphanumerical budgetid."""
        self.logger.debug('Generating an account ID')
        monthid = None
        with self.engine.connect() as conn:
            while monthid is None:
                monthid = str(random.randint(1e9, (1e10 - 1)))

                statement = self.months_table.select().where(
                    self.months_table.c.monthid == monthid
                )
                self.logger.debug('QUERY: %s', str(statement))
                result = conn.execute(statement).first()
                # If there already exists an account, try again.
                if result is not None:
                    monthid = None
                    self.logger.debug(
                        'RESULT: account ID already exists. Trying again')
        self.logger.debug('RESULT: account ID generated.')
        return monthid

    def get_month(self, monthid):
        """Get month data for the specified email.
        Params: email - the email of the user
        Return: a key/value dict of user attributes,
                {'email': email, 'userid': userid, ...}
                or None if that user does not exist
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.months_table.select().where(
            self.months_table.c.monthid == monthid)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            result = conn.execute(statement).first()
        self.logger.debug('RESULT: fetched budget data for %s', monthid)
        return dict(result) if result is not None else None
    
    def get_months(self, budgetid):
        statement = self.months_table.select().where(and_(self.months_table.c.budgetid == budgetid,self.months_table.c.parentid == None))
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            results = conn.execute(statement)
        self.logger.debug('RESULT: fetched budgets data for %s', budgetid)
        return [dict(result) for result in results] if results is not None else None

    def delete_month(self, monthid):
        """_summary_

        Args:
            budgetid (_type_): _description_
        """
        statement = self.budgets_table.delete().where(
            self.months_table.c.monthid == monthid)
        with self.engine.connect() as conn:
            results = conn.execute(statement)

        self.logger.debug('QUERY: %s', str(statement))
        return {}
    
    def update_month(self, month: dict):

        statement = self.budgets_table.update().values(month).where(
            self.months_table.c.budgetid == month["budgetid"])
        with self.engine.connect() as conn:
            results = conn.execute(statement)