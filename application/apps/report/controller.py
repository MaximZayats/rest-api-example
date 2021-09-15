from apps.report.services import (generate_report_content,
                                  generate_report_file_name)
from fastapi import APIRouter
from fastapi.responses import Response

report_router = APIRouter()


@report_router.get('/report')
async def get_report():
    return Response(
        content=await generate_report_content(),
        headers={
            'content-disposition':
                'attachment; '
                f'filename={generate_report_file_name()}',
        },
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
