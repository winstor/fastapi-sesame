from fastapi import FastAPI, Request, HTTPException


def create_app():
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI()

    # 其余的一些全局配置可以写在这里 多了可以考虑拆分到其他文件夹

    # 跨域设置
    # register_cors(app)

    # 注册路由
    # register_router(app)

    # 注册捕获全局异常
    register_exception(app)

    # 请求拦截
    # register_middleware(app)
    return app


def register_exception(app: FastAPI) -> None:
    pass


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        x_site = request.headers.get('X-SITE-AUTHORIZATION')
        if not x_site:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"www-x-site-authenticate": ""},
            )
        response = await call_next(request)
        return response
