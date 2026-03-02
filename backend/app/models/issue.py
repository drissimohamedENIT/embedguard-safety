from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    file = Column(String)
    line = Column(Integer)
    column = Column(Integer)
    severity = Column(String)
    message = Column(String)
    rule = Column(String)
    category = Column(String)
    criticality = Column(String)