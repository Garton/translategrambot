import logging
from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class UserLanguagePair(Base):
    __tablename__ = "user_language_pairs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    source_lang = Column(String(10), nullable=False)
    target_lang = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserService:
    def __init__(self):
        # For now, using SQLite. In production, use PostgreSQL
        self.engine = create_engine("sqlite:///users.db", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def set_user_language_pair(
        self, user_id: int, source_lang: str, target_lang: str
    ) -> None:
        """Save or update user's preferred language pair."""
        try:
            with self.Session() as session:
                # Check if user already has a language pair
                existing = (
                    session.query(UserLanguagePair).filter_by(user_id=user_id).first()
                )

                if existing:
                    # Update existing record
                    existing.source_lang = source_lang
                    existing.target_lang = target_lang
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new record
                    new_pair = UserLanguagePair(
                        user_id=user_id,
                        source_lang=source_lang,
                        target_lang=target_lang,
                    )
                    session.add(new_pair)

                session.commit()
                logger.info(
                    f"Saved language pair {source_lang}-{target_lang} for user {user_id}"
                )

        except Exception as e:
            logger.error(f"Error saving language pair for user {user_id}: {e}")
            raise

    async def get_user_language_pair(self, user_id: int) -> Optional[Tuple[str, str]]:
        """Get user's preferred language pair."""
        try:
            with self.Session() as session:
                user_pair = (
                    session.query(UserLanguagePair).filter_by(user_id=user_id).first()
                )

                if user_pair:
                    return (user_pair.source_lang, user_pair.target_lang)
                return None

        except Exception as e:
            logger.error(f"Error getting language pair for user {user_id}: {e}")
            return None

    async def delete_user_language_pair(self, user_id: int) -> bool:
        """Delete user's language pair preference."""
        try:
            with self.Session() as session:
                user_pair = (
                    session.query(UserLanguagePair).filter_by(user_id=user_id).first()
                )

                if user_pair:
                    session.delete(user_pair)
                    session.commit()
                    logger.info(f"Deleted language pair for user {user_id}")
                    return True
                return False

        except Exception as e:
            logger.error(f"Error deleting language pair for user {user_id}: {e}")
            return False
