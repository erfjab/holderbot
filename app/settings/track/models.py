from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StateModel(Base):
    __tablename__ = "states"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    state = Column(String)


class DataModel(Base):
    __tablename__ = "data"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    data = Column(JSON)


class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, index=True)
    message_id = Column(Integer, index=True)
