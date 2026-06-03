import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


class Connection:
    def __init__(self, env: str = "dev"):
        self.env = env
        load_dotenv(f".env.{self.env}")
        self._get_session()

    def _get_session(self):
        creds = self._get_credentials()
        conn_str = f"postgresql+psycopg2://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['dbname']}"
        self.engine = create_engine(conn_str)
        self.session = sessionmaker(bind=self.engine)()

    def _get_credentials(self):
        return {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "dbname": os.getenv("POSTGRES_DB"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
        }

    def close(self):
        self.session.close()
        self.engine.dispose()

