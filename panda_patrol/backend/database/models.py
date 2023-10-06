import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    TIMESTAMP,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

PANDA_DATABASE_URL = os.getenv("PANDA_DATABASE_URL")
Base = declarative_base()
engine = create_engine(PANDA_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    patrols = relationship("Patrol", back_populates="user")
    patrol_groups = relationship("PatrolGroup", back_populates="user")


class PatrolGroup(Base):
    __tablename__ = "patrol_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User")
    patrols = relationship("Patrol", back_populates="group")


class Patrol(Base):
    __tablename__ = "patrols"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    group_id = Column(Integer, ForeignKey("patrol_groups.id"))
    group = relationship("PatrolGroup", back_populates="patrols")
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User")
    runs = relationship("PatrolRun", back_populates="patrol")
    setting = relationship("PatrolSetting", uselist=False, back_populates="patrol")


class PatrolRun(Base):
    __tablename__ = "patrol_runs"
    id = Column(Integer, primary_key=True, index=True)
    patrol_id = Column(Integer, ForeignKey("patrols.id"))
    patrol = relationship("Patrol", back_populates="runs")
    status = Column(String, index=True)
    severity = Column(String, index=True)
    return_value = Column(Text)
    logs = Column(Text)
    patrol_code = Column(Text)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    exception = Column(Text)


class PatrolSetting(Base):
    __tablename__ = "patrol_settings"
    id = Column(Integer, primary_key=True, index=True)
    assigned_to_person = Column(Text)
    alerting = Column(Boolean, default=True)
    silenced_until = Column(TIMESTAMP)
    patrol_id = Column(Integer, ForeignKey("patrols.id"), unique=True)
    patrol = relationship("Patrol", back_populates="setting")
    parameters = relationship("PatrolParameter", back_populates="setting")


class PatrolParameter(Base):
    __tablename__ = "patrol_parameters"
    id = Column(Integer, primary_key=True, index=True)
    parameter_id = Column(Text, index=True)
    value = Column(Text)
    type = Column(String, index=True)
    default_value = Column(Text)
    setting_id = Column(Integer, ForeignKey("patrol_settings.id"))
    setting = relationship("PatrolSetting", back_populates="parameters")
