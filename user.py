#!/usr/bin/env python3
"""
User model for SQLAlchemy
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy User model that maps to the users table
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

# Ensure this file can be run to print the table structure
if __name__ == "__main__":
    print(User.__tablename__)
    for column in User.__table__.columns:
        print(f"{column}: {column.type}")
