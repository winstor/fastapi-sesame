from fastapi import FastAPI, Request
from .custom_exc import *


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        response = await call_next(request)
        return response


def register_static_file(app: FastAPI) -> None:
    # 自定义异常 捕获
    @app.exception_handler(UserNotFound)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFound):
        pass

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        pass

