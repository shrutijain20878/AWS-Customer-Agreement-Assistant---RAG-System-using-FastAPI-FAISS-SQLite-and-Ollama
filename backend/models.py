from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    Float,
    DateTime
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class QueryLog(Base):

    __tablename__ = "query_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    query = Column(Text)

    answer = Column(Text)

    answer_found = Column(Boolean)

    latency_ms = Column(Float)

    retrieved_chunks = Column(Integer)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )