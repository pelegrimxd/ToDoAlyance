from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from backend.models.static import TaskStatus
from backend.models.db_models.base import Base, int_pk, str_uniq, str_null_true, date_time


class Task(Base):
    id: Mapped[int_pk]
    title: Mapped[str_uniq]
    description: Mapped[str_null_true]
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.todo.value, nullable=False)
    due_date: Mapped[date_time]
    owner: Mapped[int]

    def __repr__(self):
        return str(self)