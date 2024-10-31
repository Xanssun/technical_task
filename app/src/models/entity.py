import logging
import random
import string
import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from core.settings import settings
from db.postgres import Base
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password) 
    
    @staticmethod
    def hash_password(password: str) -> str:
        # Генерация соли и хеширование пароля
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        # Проверка пароля
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum("in_progress", "completed", name="task_status"), default="in_progress")

    user_id = Column(UUID, ForeignKey('users.id'))
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"


class Token:
    def __init__(
        self, user_id: int = None, token: str = None
    ):
        if token:
            try:
                decoded = jwt.decode(
                    token,
                    settings.auth_secret,
                    algorithms=['HS256'],
                )
            except Exception as error:
                logging.error(f'Smth wrong with token = {error}')
                decoded = {}
            if (
                decoded.get('user_id')

                and decoded.get('expires')
            ):
                self.user_id = decoded['user_id']
                self.expires = decoded['expires']
                self.token = token
            else:
                self.user_id = 'invalid_token'
                self.expires = '0000-00-00 00:00:00'
                self.token = token
        else:
            self.user_id = user_id
            expires = datetime.now() + timedelta(
                seconds=settings.auth_token_lifetime
            )
            self.expires = expires.strftime('%Y-%m-%d %H:%M:%S')
            self.token = self.create_token()

    def create_token(self) -> str:
        return jwt.encode(
            {
                'user_id': str(self.user_id),
                'expires': self.expires,
            },
            settings.auth_secret,
            algorithm='HS256',
        )

    def is_expired(self) -> bool:
        if self.expires >= datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            return False
        return True

    def __repr__(self) -> str:
        return f"<Token {self.user_id}, expires = {self.expires}>"


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    expires = Column(DateTime, default=datetime.utcnow)
    refresh_token = Column(String(250))
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    def __init__(
        self, user_id: str, expires: datetime = None, refresh_token: str = None
    ):
        self.expires = expires
        self.refresh_token = refresh_token
        self.user_id = user_id

    def regenerate(self):
        self.refresh_token = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(settings.auth_refresh_token_length)
        )
        self.expires = datetime.now() + timedelta(
            seconds=settings.auth_refresh_token_lifetime
        )

    def __repr__(self) -> str:
        return f'<RefreshToken {self.refresh_token} expires { self.expires }>'
