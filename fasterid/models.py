from sqlalchemy import Column, ForeignKey, Integer, String

from fasterid.database import Base

# from sqlalchemy.orm import relationship



class Erdi8(Base):
    __tablename__ = "erdi8s"

    id = Column(Integer, primary_key=True, index=True)
    prefix_id = Column(Integer, ForeignKey("prefixes.id"))
    key = Column(String, unique=True)
    erdi8 = Column(String, unique=True)


class Prefix(Base):
    __tablename__ = "prefixes"

    id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String, unique=True, index=True, nullable=True)
    last_erdi8 = Column(String, unique=True, index=True)
