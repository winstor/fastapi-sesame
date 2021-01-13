from typing import Callable
from fastapi import Request, Response, HTTPException, Depends
from fastapi.routing import APIRoute
from app.api.deps import oauth2_scheme
from app.core import security


class CheckTokenHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        call_next = super().get_route_handler()

        async def app_route_handler(request: Request) -> Response:
            try:
                # # 检测账号
                # token = await oauth2_scheme.__call__(request)
                # print(token)
                # print(222222222222222222222222222)
                # security.token_decode(token)

                response: Response = await call_next(request)
            except Exception as exc:
                body = await request.body()
                raise HTTPException(status_code=400, detail='no Find')
            # print(f"route response headers: {response.headers}")
            return response

        return app_route_handler
