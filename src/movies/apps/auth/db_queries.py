from sqlalchemy.orm import Session
from .models import RevokedToken
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


def add_revoked_token(db: Session, token: str):
    revoked = RevokedToken(token=token)
    db.add(revoked)
    try:
        db.commit()
        db.refresh(revoked)
        return revoked
    except IntegrityError:
        db.rollback()
        return None


def is_token_revoked(db: Session, token: str) -> bool:
    stmt = select(RevokedToken).where(RevokedToken.token == token)
    result = db.execute(stmt)
    return result.scalar_one_or_none() is not None

