from fastapi import FastAPI
import logging
from backend.api.task_api import router as task_router
from backend.api.task_admin_api import router as task_admin_router

app = FastAPI()

def configure_logging(level):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)4d %(levelname)-8s - %(message)s",
    )

def main(_app: FastAPI):
    configure_logging(logging.INFO)
    _app.include_router(task_router, prefix="/tasks")
    _app.include_router(task_admin_router, prefix="/tasks_admin")

main(app)