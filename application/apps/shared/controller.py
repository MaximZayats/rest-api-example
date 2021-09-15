from fastapi import APIRouter
from fastapi.responses import RedirectResponse

shared_router = APIRouter()


@shared_router.get('/', include_in_schema=False)
async def redirect():
    return RedirectResponse(url='/docs')
