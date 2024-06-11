from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "tb_users"

    idUser = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    telegram_id = Column(String(length=255))
    email = Column(String(length=255))
    asistant_name = Column(String(length=255))
    selected_asistant_role = Column(Integer)

class ChatLog(Base):
    __tablename__ = "tb_chat_log"

    idChatLog = Column(Integer, primary_key=True)
    relIdUser = Column(Integer)
    text = Column(Text)
    timestamp = Column(String(length=50))


class AsistantRoles(Base):
    __tablename__ = "tb_asistant_roles"

    idAsistantRole = Column(Integer, primary_key=True)
    AsistantRole = Column(Text)
    AsistantRoleDescription = Column(String(length=255))


class UserThreads(Base):
    __tablename__ = "tb_user_threads"

    idUserThread = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    thread_id = Column(String(length=255))