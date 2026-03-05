from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    stored_as = Column(String, nullable=False)

    file_hash = Column(String, unique=True, index=True)   # ⭐ NEW

    score = Column(Integer, nullable=False)
    status = Column(String, default="processing")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    issues = relationship("Issue", backref="analysis", cascade="all, delete")