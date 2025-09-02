from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from datetime import datetime

engine = create_engine('postgresql+psycopg2://postgres:Edikri11*)@localhost:5432/ai_assistant', echo=True)
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True) 
    title = Column(String, nullable=False) 
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow) 
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=False) 
    priority = Column(Integer, default=3)
    category = Column(String)

    def __repr__(self):
        return f"<Task(title='{self.title}', completed={self.is_completed})>"
    
class Complited(Base):
    __tablename__ = 'complited'
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False) 
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow) 
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=True) 
    priority = Column(Integer, default=3)
    category = Column(String)
    
    def __repr__(self):
        return f"<Task(title='{self.title}', completed={self.is_completed})>"
    
Base.metadata.create_all(engine)