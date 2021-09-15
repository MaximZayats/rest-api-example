from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union

from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from . import tortoise as tortoise_models


class _AllFieldsOptionalMeta(type(PydanticModel), type):  # type: ignore
    """Metaclass for changing all fields to Optional"""

    BASE_MODEL = PydanticModel

    def __new__(mcs, name: str, bases: Tuple[type, ...], namespaces: Dict[str, Any], **kwargs):
        annotations: dict = namespaces.get('__annotations__', {})

        for base in bases:
            annotations.update(base.__annotations__)

            for base_ in base.__mro__:
                if base_ is mcs.BASE_MODEL:
                    break

                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]

        namespaces['__annotations__'] = annotations

        return super().__new__(mcs, name, bases, namespaces, **kwargs)


class Task:
    _BaseTask = pydantic_model_creator(
        tortoise_models.Task, name='_BaseTask', exclude=('id',)
    )

    class _Base(_BaseTask):  # type: ignore
        class Config:
            title = 'Abstract Base Task'

    class Out(_Base):
        id: int

        class Config:
            title = 'Task Output'

    class Create(_Base):
        id: Optional[int]

        class Config:
            title = 'Task Create'

    class PutUpdate(_Base):
        class Config:
            title = 'Task Put Update'

    class PatchUpdate(_Base, metaclass=_AllFieldsOptionalMeta):
        class Config:
            title = 'Task Patch Update'

    class Select(_Base, metaclass=_AllFieldsOptionalMeta):
        id: Optional[int]
        name__contains: Optional[str]

        start_date__gt: Optional[Union[datetime, int]]
        start_date__gte: Optional[Union[datetime, int]]
        start_date__lt: Optional[Union[datetime, int]]
        start_date__lte: Optional[Union[datetime, int]]

        end_date__gt: Optional[Union[datetime, int]]
        end_date__gte: Optional[Union[datetime, int]]
        end_date__lt: Optional[Union[datetime, int]]
        end_date__lte: Optional[Union[datetime, int]]

        class Config:
            title = 'Select Task'


class TaskElement:
    _BaseTaskElement = pydantic_model_creator(
        tortoise_models.TaskElement, name='_BaseTaskElement', exclude=('id', 'task_id')
    )

    class _Base(_BaseTaskElement):  # type: ignore
        class Config:
            title = 'Abstract Task Element'

    class Out(_Base):
        task_id: int
        id: int

        class Config:
            title = 'Task Element Out'

    class Create(_Base):
        id: Optional[int]

        class Config:
            title = 'Task Element Create'

    class PutUpdate(_Base):
        class Config:
            title = 'Task Element Put Update'

    class PatchUpdate(_Base, metaclass=_AllFieldsOptionalMeta):
        class Config:
            title = 'Task Element Patch Update'

    class Select(_Base, metaclass=_AllFieldsOptionalMeta):
        id: Optional[int]
        task_id: int = 0
        value__contains: Optional[str]

        class Config:
            title = 'Task Element Select'
