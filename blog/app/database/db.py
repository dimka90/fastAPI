from sqlmodel import SQLModel, Session, create_engine

engine = create_engine(database_url)

def create_session():
    return Session

