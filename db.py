from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///boardgames.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Queue(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    bgg_url = Column(Integer, unique=True, nullable=False)
    min_players = Column(Integer, nullable=False)
    max_players = Column(Integer, nullable=False)
    min_playtime = Column(Integer, nullable=False)
    max_playtime = Column(Integer, nullable=False)    

Base.metadata.create_all(engine)
