from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_database_if_missing():
    """Create the MySQL database if it does not already exist. Handle connection errors gracefully."""
    try:
        server_url = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/mysql"
        )
        engine_server = create_engine(server_url, future=True)
        database_name = MYSQL_DB.replace('`', '')

        with engine_server.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database_name}`"))
            connection.commit()
            print(f"✓ Database '{database_name}' ready")
    except Exception as e:
        print(f"⚠ Database connection error (will retry on startup): {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
