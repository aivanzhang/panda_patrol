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
engine = create_engine(
    PANDA_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    email = Column(Text, index=True)


class PatrolGroup(Base):
    __tablename__ = "patrol_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    patrols = relationship("Patrol", back_populates="group")


class Patrol(Base):
    __tablename__ = "patrols"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    group_id = Column(Integer, ForeignKey("patrol_groups.id"))
    group = relationship("PatrolGroup", back_populates="patrols")
    runs = relationship("PatrolRun", back_populates="patrol")
    profiles = relationship("PatrolProfile", back_populates="patrol")
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


class PatrolProfile(Base):
    __tablename__ = "patrol_profiles"
    id = Column(Integer, primary_key=True, index=True)
    patrol_id = Column(Integer, ForeignKey("patrols.id"))
    patrol = relationship("Patrol", back_populates="profiles")
    report = Column(Text)
    time = Column(TIMESTAMP)
    format = Column(String, index=True)


class PatrolSetting(Base):
    __tablename__ = "patrol_settings"
    id = Column(Integer, primary_key=True, index=True)
    assigned_to_person = Column(Integer, ForeignKey("people.id"))
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
    is_active = Column(Boolean, default=True)
    setting_id = Column(Integer, ForeignKey("patrol_settings.id"))
    setting = relationship("PatrolSetting", back_populates="parameters")
