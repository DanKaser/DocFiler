import os
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db import Base
from src.models.tags import TagDocType

class Document(Base):

    __tablename__ = 'document'

    __tabel_args__ = {UniqueConstraint('filename', 'rel_path')}

    filename: Mapped[str] = mapped_column()
    rel_path: Mapped[str] = mapped_column()

    doc_type_id: Mapped[int] = mapped_column(ForeignKey('doctype.id'),
                                             nullable=False)
    doc_type: Mapped[TagDocType] = relationship()

    @property
    def abs_path(self) -> str:
        return os.path.join(os.getcwd(), self.rel_path, self.filename)

    @property
    def name(self) -> str:
        return os.path.split(self.filename)[0]
