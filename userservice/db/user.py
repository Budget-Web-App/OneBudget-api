import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, LargeBinary, and_
import random
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

class UserDb:
    """
    UserDb provides a set of helper functions over SQLAlchemy
    to handle db operations for userservice
    """

    def __init__(self, uri, logger=logging):
        self.engine = create_engine(uri)
        self.logger = logger
        self.users_table = Table(
            'users',
            MetaData(self.engine),
            Column('userid', String, primary_key=True),
            Column('email', String, unique=True, nullable=False),
            Column('passhash', LargeBinary, nullable=False),
            Column('timezone', String, nullable=False),
            Column('registereddate', Date, nullable=True),
        )
        # Set up tracing autoinstrumentation for sqlalchemy
        SQLAlchemyInstrumentor().instrument(
            engine=self.engine,
            service='users',
        )

    def add_user(self, user):
        """Add a user to the database.
        Params: user - a key/value dict of attributes describing a new user
                    {'email': email, 'password': password, ...}
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.users_table.insert().values(user)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            conn.execute(statement)

    def generate_userid(self):
        """Generates a globally unique alphanumerical userid."""
        self.logger.debug('Generating an account ID')
        userid = None
        with self.engine.connect() as conn:
            while userid is None:
                userid = str(random.randint(1e9, (1e10 - 1)))

                statement = self.users_table.select().where(
                    self.users_table.c.userid == userid
                )
                self.logger.debug('QUERY: %s', str(statement))
                result = conn.execute(statement).first()
                # If there already exists an account, try again.
                if result is not None:
                    userid = None
                    self.logger.debug(
                        'RESULT: account ID already exists. Trying again')
        self.logger.debug('RESULT: account ID generated.')
        return userid

    def get_user(self, email):
        """Get user data for the specified email.
        Params: email - the email of the user
        Return: a key/value dict of user attributes,
                {'email': email, 'userid': userid, ...}
                or None if that user does not exist
        Raises: SQLAlchemyError if there was an issue with the database
        """
        statement = self.users_table.select().where(
            self.users_table.c.email == email)
        self.logger.debug('QUERY: %s', str(statement))
        with self.engine.connect() as conn:
            result = conn.execute(statement).first()
        self.logger.debug('RESULT: fetched user data for %s', email)
        return dict(result) if result is not None else None
