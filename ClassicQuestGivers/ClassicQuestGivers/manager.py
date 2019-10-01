from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from scrapy import Item
from .db import Quest


class Manager:
    session: Session

    def __init__(self, engine_adress: str):
        self.engine = create_engine(engine_adress)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.session.close()

    def open(self):
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()

    def get_quest(self, level: int, levels_hihger=2, levels_lower=2, zone: str = None):
        pass

    def add_quest(self, item: Item):
        exists = self.session.query(Quest.id).filter_by(id=item["id"]).all()
        if not exists:
            quest = Quest(**dict(item))
            self.session.add(quest)
            self.session.commit()
