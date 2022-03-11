from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


class Promo(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180))
    description = Column(String(5000), nullable=True)
    prizes = relationship("Prize", backref="prizes", lazy=True)
    participants = relationship("Participant", backref="participants", lazy=True)


class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(5000))
    promo_id = Column(Integer, ForeignKey("promos.id"))


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180))
    promo_id = Column(Integer, ForeignKey("promos.id"))


book_authors = Table(
    "results",
    Base.metadata,
    Column("winner", ForeignKey("participants.id"), primary_key=True),
    Column("prize", ForeignKey("prizes.id"), primary_key=True),
)
