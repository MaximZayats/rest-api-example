from fastapi.requests import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


async def does_not_exist_exception_handler(request: Request, exc: DoesNotExist):  # NOQA  # type: ignore
    return JSONResponse(status_code=404, content={'detail': str(exc)})


async def integrity_error_exception_handler(request: Request, exc: IntegrityError):  # NOQA  # type: ignore
    return JSONResponse(
        status_code=409,
        content={'detail': [{'loc': [], 'msg': str(exc), 'type': 'IntegrityError'}]},
    )
