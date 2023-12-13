from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///boardgames.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

user_game_association = Table('user_game', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    games = relationship("Games", secondary=user_game_association, back_populates="owners")

class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    bgg_url = Column(Integer, unique=True, nullable=False)
    min_players = Column(Integer, nullable=False)
    max_players = Column(Integer, nullable=False)
    min_playtime = Column(Integer, nullable=False)
    max_playtime = Column(Integer, nullable=False)
    owners = relationship("User", secondary=user_game_association, back_populates="games")

Base.metadata.create_all(engine)
