import os
from sqlalchemy import ...
from sqlalchemy.orm import mapped_column, Mapped

from src.db import Base

class Document(Base):

    filename: Mapped[str] = mapped_column()
    rel_path: Mapped[str] = mapped_column()

    @property
    def full_path(self) -> str:
        return os.path.join(self.rel_path, self.filename)

    @property
    def name(self) -> str:
        return os.path.split(self.filename)[0]