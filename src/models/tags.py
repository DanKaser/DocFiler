from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

TaginfoXDocument = Table(
    'taginfoxdocument',
    Base.metadata,
    Column('taginfo_id', Integer,
        ForeignKey('taginfo.id'), primary_key = True),
    Column('document_id', Integer,
        ForeignKey('document.id'), primary_key = True))

class AbstractTag(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(unique=True)

class TagDocType(AbstractTag):
    __tablename__ = 'doctype'

class TagInfo(AbstractTag):
    __tablename__ = 'taginfo'

