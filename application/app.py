import asyncio
from os import getenv
from typing import Callable, Optional

import uvicorn
from apps.core.controller import tasks_elements_router, tasks_router
from apps.report.controller import report_router
from apps.shared import exception_handlers
from apps.shared.controller import shared_router
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError


def init_database(application: FastAPI) -> Callable[..., None]:
    def _init():
        load_dotenv()

        db_url: Optional[str] = getenv('DB_URL')

        if db_url is None:
            raise ValueError('Specify "db_url" in the ".env" file.')

        application.add_exception_handler(DoesNotExist, exception_handlers.does_not_exist_exception_handler)
        application.add_exception_handler(IntegrityError, exception_handlers.integrity_error_exception_handler)

        register_tortoise(
            app=application,
            db_url=db_url,
            modules={'models': ['apps.core.models.tortoise']},
            generate_schemas=True,
            add_exception_handlers=False,
        )

    return _init


def init_routers(application: FastAPI) -> None:
    application.include_router(
        tasks_elements_router, tags=['Task Elements'])
    application.include_router(
        tasks_router, tags=['Tasks'])

    application.include_router(
        report_router, tags=['Report'])

    application.include_router(
        shared_router, include_in_schema=False)


def get_application() -> FastAPI:
    application = FastAPI(title='RestAPI example')

    application.add_event_handler("startup", init_database(application))

    init_routers(application)

    return application


async def run_server(application: FastAPI) -> None:
    config = uvicorn.Config(app=application, host='0.0.0.0', port=80)
    server = uvicorn.Server(config=config)

    await server.serve()


app = get_application()


if __name__ == '__main__':
    asyncio.run(run_server(app))
