from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from db import Base

class RevokedToken(Base):
    __tablename__ = "revoked_token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)



