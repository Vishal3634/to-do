from sqlalchemy import create_engine
# connection between your python and specific database
from sqlalchemy.ext.declarative import declarative_base
# declarative_base() creates a parent class so SQLAlchemy knows which Python classes should become database tables.
from sqlalchemy.orm import sessionmaker 
# sessionmaker configures and generates Session objects that are used to interact with the database in SQLAlchemy.

database_url="postgresql://neondb_owner:npg_fdzyigHp3FU5@ep-lucky-band-a18mxg2m-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine=create_engine(database_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


