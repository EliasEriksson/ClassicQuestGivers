from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from scrapy import Item
from .db import Quest
from . import DATABASE_ADRESS


class Manager:
    session: Session

    def __init__(self, engine_adress: str = DATABASE_ADRESS):
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

    @staticmethod
    def format_zone(zone: str) -> str:
        if zone:
            return zone.lower().replace(" ", "-").replace("'", "")

    def get_quest(self, level: int, faction: str = "N", levels_higher=2, levels_lower=2, zone: str = None):
        upper = 60 if level + levels_higher > 60 else level + levels_higher
        lower = 1 if level - levels_lower < 1 else level - levels_lower
        zone = self.format_zone(zone)

        conditions = [Quest.level <= upper,
                      lower <= Quest.level,
                      Quest.faction.in_(list(faction))]
        if zone:
            conditions.append(Quest.zone == zone)

        return self.session.query(Quest).filter(*conditions).order_by(Quest.level.asc()).all()

    def add_quest(self, item: Item):
        exists = self.session.query(Quest.id).filter_by(id=item["id"]).all()
        if not exists:
            quest = Quest(**dict(item))
            self.session.add(quest)
            self.session.commit()


