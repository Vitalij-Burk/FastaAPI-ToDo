import uuid
from enum import Enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Status(str, Enum):
    Zero = "Zero"
    Active = "Active"
    Verify = "Verify"
    Completed = "Completed"


class MyBase(Base):
    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    async def is_active_property(self):
        if self.is_active is False:
            return False
        return True


class User(MyBase):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    created_tasks = relationship(
        "UserCreatedTask", back_populates="user", lazy="selectin"
    )
    assigned_tasks = relationship(
        "UserAssignedTask", back_populates="user", lazy="selectin"
    )


class Task(MyBase):
    __tablename__ = "tasks"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task = Column(String, nullable=False)
    status = Column(String, default=Status.Zero)

    authors = relationship("UserCreatedTask", back_populates="task", lazy="selectin")
    producers = relationship("UserAssignedTask", back_populates="task", lazy="selectin")

    async def next_status_level(self) -> str:
        match self.status:
            case Status.Zero:
                return Status.Active
            case Status.Active:
                return Status.Verify
            case Status.Verify:
                return Status.Completed


class UserCreatedTask(Base):
    __tablename__ = "user_created_tasks"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.task_id"), primary_key=True)

    user = relationship("User", back_populates="created_tasks")
    task = relationship("Task", back_populates="authors")


class UserAssignedTask(Base):
    __tablename__ = "user_assigned_tasks"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.task_id"), primary_key=True)

    user = relationship("User", back_populates="assigned_tasks")
    task = relationship("Task", back_populates="producers")
