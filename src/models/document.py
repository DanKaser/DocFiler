import os
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from src.db import Base

class Document(Base):

    __tablename__ = 'document'

    __tabel_args__ = {UniqueConstraint('filename', 'rel_path')}

    filename: Mapped[str] = mapped_column()
    rel_path: Mapped[str] = mapped_column()

    @property
    def abs_path(self) -> str:
        return os.path.join(os.getcwd(), self.rel_path, self.filename)

    @property
    def name(self) -> str:
        return os.path.split(self.filename)[0]
