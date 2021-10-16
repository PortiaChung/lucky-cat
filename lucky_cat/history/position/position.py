from sqlalchemy import Column, Integer, String, FLOAT
from lucky_cat.history import base

class OpenPosition(base.Base):
    __tablename__ = 'open_position'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    open_price = Column(FLOAT)
    count = Column(Integer)


class ClosedPosition(base.Base):
    __tablename__ = 'closed_position'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    open_price = Column(FLOAT)
    close_price = Column(FLOAT)
