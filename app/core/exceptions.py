from typing import Any, Dict, Optional, Sequence
from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(
            self,
            detail: Any,
            headers: Optional[Dict[str, Any]] = None,
            status_code: int = status.HTTP_401_UNAUTHORIZED,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class ErrorException(HTTPException):
    def __init__(
            self,
            detail: Any,
            headers: Optional[Dict[str, Any]] = None,
            status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class RepeatException(HTTPException):
    def __init__(
            self,
            detail: Any,
            headers: Optional[Dict[str, Any]] = None,
            status_code: int = status.HTTP_409_CONFLICT,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class TimeOutException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
            status_code: int = status.HTTP_408_REQUEST_TIMEOUT,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers
