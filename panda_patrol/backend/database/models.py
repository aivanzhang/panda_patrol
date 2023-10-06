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
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)


class PatrolGroup(Base):
    __tablename__ = "patrol_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    user_id = Column(String, ForeignKey("users.id"))


class Patrol(Base):
    __tablename__ = "patrols"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    group_id = Column(Integer, ForeignKey("patrol_groups.id"))
    user_id = Column(String, ForeignKey("users.id"))


class PatrolRun(Base):
    __tablename__ = "patrol_runs"
    id = Column(Integer, primary_key=True, index=True)
    patrol_id = Column(Integer, ForeignKey("patrols.id"))
    status = Column(String, index=True)
    severity = Column(String, index=True)
    return_value = Column(Text)
    logs = Column(Text)
    patrol_code = Column(Text)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    exception = Column(Text)


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    emails = Column(Text)  # Comma-separated emails
    other_settings = Column(Text)  # JSON string


class PatrolSetting(Base):
    __tablename__ = "patrol_settings"
    id = Column(Integer, primary_key=True, index=True)
    assigned_to_person = Column(Text)
    alerting = Column(Boolean, default=True)
    silenced_until = Column(TIMESTAMP)
    patrol_id = Column(Integer, ForeignKey("patrols.id"), unique=True)


class PatrolParameter(Base):
    __tablename__ = "patrol_parameters"
    id = Column(Integer, primary_key=True, index=True)
    parameter_id = Column(Text, index=True)
    setting_id = Column(Integer, ForeignKey("patrol_settings.id"))
    value = Column(Text)
    type = Column(String, index=True)
    default_value = Column(Text)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
