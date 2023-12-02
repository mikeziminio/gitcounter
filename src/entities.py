from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import Date
import uuid
import datetime


class Base(DeclarativeBase):
    pass


class Repo(Base):
    __tablename__ = "repo"

    id: Mapped[uuid.UUID] = mapped_column(type_=postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    stats: Mapped[set["RepoStat"]] = relationship(back_populates="repo", )


class RepoStat(Base):
    __tablename__ = "repo_stat"

    id: Mapped[uuid.UUID] = mapped_column(type_=postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("repo.id"))
    repo: Mapped[Repo] = relationship(back_populates="stats")
    stat_date: Mapped[datetime.date] = mapped_column(type_=Date)
    new_lines: Mapped[int | None]

