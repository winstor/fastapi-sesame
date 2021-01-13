from fastapi import HTTPException


class ApiResponse:

    @staticmethod
    def status(*, status: bool, data: dict):
        status = status and 1 or 0
        data.update({"status": status})
        return data

    @staticmethod
    def api_massage(massage: str):
        return ApiResponse.status(data={"massage": massage}, status=True)

    @staticmethod
    def api_failed(massage: str):
        return ApiResponse.status(data={"massage": massage}, status=False)

    @staticmethod
    def api_success(data):
        if isinstance(data, str):
            return ApiResponse.status(data={"massage": data}, status=True)
        if isinstance(data, (dict, list)):
            return ApiResponse.status(data={"data": data}, status=False)
        raise HTTPException(status_code=400, detail="api_success 返回参数类型错误")