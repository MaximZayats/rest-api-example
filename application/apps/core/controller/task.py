from typing import List

from apps.core.models.pydantic import Task as TaskPydantic
from apps.core.models.tortoise import Task
from apps.shared import responses
from apps.shared.services import (create_object, delete_object, get_object,
                                  get_objects, patch_update, put_update)
from fastapi import APIRouter, Depends
from fastapi.responses import Response

tasks_router = APIRouter()


@tasks_router.get('/tasks/{task_id}',
                  response_model=TaskPydantic.Out,
                  responses=responses.Response.GET_BY_ID)
async def get_task(task_id: int):
    return await get_object(Task, TaskPydantic.Out, id=task_id)


@tasks_router.get('/tasks',
                  response_model=List[TaskPydantic.Out],
                  responses=responses.Response.GET_LIST)
async def get_tasks(select_task: TaskPydantic.Select = Depends(TaskPydantic.Select)):
    return await get_objects(
        Task, TaskPydantic.Out, **select_task.dict(exclude_none=True)
    )


@tasks_router.post('/tasks',
                   response_model=TaskPydantic.Out,
                   status_code=201,
                   responses=responses.Response.POST)
async def create_task(task: TaskPydantic.Create):
    return await create_object(
        Task, TaskPydantic.Out, **task.dict(exclude_unset=True)
    )


@tasks_router.put('/tasks/{task_id}',
                  status_code=204,
                  responses=responses.Response.PUT)
async def update_task(task_id: int, task: TaskPydantic.PutUpdate):
    await put_update(Task, task, id=task_id)
    return Response(status_code=204)


@tasks_router.patch('/tasks/{task_id}',
                    response_model=TaskPydantic.Out,
                    responses=responses.Response.PATCH)
async def patch_task(task_id: int, task: TaskPydantic.PatchUpdate):
    return await patch_update(
        Task, task, TaskPydantic.Out, id=task_id
    )


@tasks_router.delete('/tasks/{task_id}',
                     responses=responses.Response.DELETE,
                     status_code=204)
async def delete_task(task_id: int):
    await delete_object(Task, task_id)
    return Response(status_code=204)
