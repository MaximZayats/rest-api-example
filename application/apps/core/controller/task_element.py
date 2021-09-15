from typing import List

from apps.core.models.pydantic import TaskElement as TaskElementPydantic
from apps.core.models.tortoise import TaskElement
from apps.shared import responses
from apps.shared.services import (create_object, delete_object, get_object,
                                  get_objects, patch_update, put_update)
from fastapi import APIRouter, Depends
from fastapi.responses import Response

tasks_elements_router = APIRouter()


@tasks_elements_router.get('/tasks/elements/{task_element_id}',
                           response_model=TaskElementPydantic.Out,
                           responses=responses.Response.GET_BY_ID)
async def get_task_element_by_id(task_element_id: int):
    return await get_object(
        TaskElement, TaskElementPydantic.Out, id=task_element_id
    )


@tasks_elements_router.get('/tasks/{task_id}/elements',
                           response_model=List[TaskElementPydantic.Out],
                           responses=responses.Response.GET_LIST)
async def get_task_elements_by_task_id(task_id: int):
    return await get_objects(
        TaskElement, TaskElementPydantic.Out,
        task_id=task_id
    )


@tasks_elements_router.get('/tasks/elements',
                           response_model=List[TaskElementPydantic.Out],
                           responses=responses.Response.GET_LIST)
async def get_task_elements(
        select_task_element: TaskElementPydantic.Select = Depends(TaskElementPydantic.Select)):
    return await get_objects(
        TaskElement, TaskElementPydantic.Out,
        **select_task_element.dict(exclude_none=True)
    )


@tasks_elements_router.post('/tasks/{task_id}/elements',
                            response_model=TaskElementPydantic.Out,
                            status_code=201,
                            responses=responses.Response.POST)
async def create_task_element(task_id: int, task_element: TaskElementPydantic.Create):
    return await create_object(
        TaskElement, TaskElementPydantic.Out,
        task_id=task_id, **task_element.dict(exclude_unset=True)
    )


@tasks_elements_router.delete('/tasks/elements/{task_element_id}',
                              responses=responses.Response.DELETE,
                              status_code=204)
async def delete_task(task_element_id: int):
    await delete_object(TaskElement, task_element_id)
    return Response(status_code=204)


@tasks_elements_router.put('/tasks/elements/{task_element_id}',
                           status_code=204,
                           responses=responses.Response.PUT)
async def update_task(task_element_id: int, task_element: TaskElementPydantic.PutUpdate):
    await put_update(TaskElement, task_element, id=task_element_id)
    return Response(status_code=204)


@tasks_elements_router.patch('/tasks/elements/{task_element_id}',
                             response_model=TaskElementPydantic.Out,
                             responses=responses.Response.PATCH)
async def patch_task(task_element_id: int, task_element: TaskElementPydantic.PatchUpdate):
    return await patch_update(
        TaskElement, task_element, TaskElementPydantic.Out, id=task_element_id
    )
