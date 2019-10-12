from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    link = Column(String)
    level = Column(Integer)
    req = Column(Integer)
    faction = Column(String)
    npc = Column(String)
    npc_link = Column(String)
    repeatable = Column(Boolean)
    zone = Column(String)
    requirements = relationship("Requirement", back_populates=__tablename__)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, engine):
        cls.metadata.create_all(engine)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, {self.name}, {self.link})"


class Requirement(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    requirement_for = Column(Integer, ForeignKey("quests.id"))
    quest_id = Column(Integer)
    quests = relationship("Quest", back_populates=__tablename__)

    @classmethod
    def create(cls, engine):
        cls.metadata.create_all(engine)


if __name__ == '__main__':
    from pathlib import Path

    PROJECT_ROOT = Path(__file__).absolute().parent.parent.parent
    DATABASE_ADRESS = f'sqlite:////{str(PROJECT_ROOT.joinpath("db.db"))}'

    e = create_engine(DATABASE_ADRESS)

    Quest.create(e)
    Requirement.create(e)
