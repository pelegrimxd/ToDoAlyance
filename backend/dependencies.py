from backend.core.settings import app_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.models.db_models.task import Task
from backend.services.domain.task_manager.task_manager_service import TaskManager
from backend.services.infrastructure.task_database.task_database_repository import TaskRepository

DB_HOST = app_config.postgres_host
DB_PORT = app_config.postgres_port
DB_NAME = app_config.postgres_db
DB_USER = app_config.postgres_user
DB_PASSWORD = app_config.postgres_password

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@postgres_database:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

task_repo: TaskRepository = TaskRepository(
    model = Task,
    session_maker=async_session_maker
)

task_manager: TaskManager = TaskManager(
    task_repo=task_repo
)