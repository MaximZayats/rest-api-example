from typing import Any, List, Type

from fastapi import HTTPException, status
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel
from tortoise.exceptions import DoesNotExist


async def get_object(
        database_model_type: Type[Model],
        pydantic_model_type: Type[PydanticModel],
        **query_params: Any,
) -> PydanticModel:
    return await pydantic_model_type.from_queryset_single(
        database_model_type.get(**query_params)
    )


async def get_objects(
        database_model_type: Type[Model],
        pydantic_model_type: Type[PydanticModel],
        **query_params: Any,
) -> List[PydanticModel]:
    return await pydantic_model_type.from_queryset(
        database_model_type.filter(**query_params).all()
    )


async def create_object(
        database_model_type: Type[Model],
        pydantic_model_type: Type[PydanticModel],
        **query_params: Any,
) -> PydanticModel:
    obj = await database_model_type.create(**query_params)

    return await pydantic_model_type.from_tortoise_orm(obj)


async def delete_object(
        database_model_type: Type[Model],
        object_id: int
) -> None:
    successfully = await database_model_type.filter(id=object_id).delete()

    if not successfully:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


async def _update_object(
        database_model_type: Type[Model],
        pydantic_model_with_new_data: PydanticModel,
        **filter_params: Any,
) -> bool:
    update_params = pydantic_model_with_new_data.dict(exclude_unset=True)

    if not update_params:
        return False

    rows_updates = await database_model_type.filter(
        **filter_params
    ).update(**update_params)

    if not rows_updates:
        raise DoesNotExist('Object does not exist')

    return bool(rows_updates)


async def patch_update(
        database_model_type: Type[Model],
        pydantic_model_with_new_data: PydanticModel,
        pydantic_out_model: Type[PydanticModel],
        **filter_params: Any,
) -> PydanticModel:
    await _update_object(
        database_model_type, pydantic_model_with_new_data, **filter_params
    )

    return await get_object(
        database_model_type, pydantic_out_model, **filter_params
    )


async def put_update(
        database_model_type: Type[Model],
        pydantic_model_with_new_data: PydanticModel,
        **filter_params: Any,
) -> None:
    await _update_object(
        database_model_type, pydantic_model_with_new_data, **filter_params
    )
