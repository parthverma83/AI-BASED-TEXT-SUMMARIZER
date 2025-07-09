from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    summaries = relationship('Summary', back_populates='user')
    feedbacks = relationship('Feedback', back_populates='user')

class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    original_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    user = relationship('User', back_populates='summaries')

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    feedback = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    user = relationship('User', back_populates='feedbacks')
