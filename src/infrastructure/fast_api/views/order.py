from typing import Annotated

from fastapi import APIRouter, HTTPException, status as status_code, Depends, BackgroundTasks

from src.domain.shared.exceptions.base import DomainException

from src.infrastructure.redis.repositories.order import OrderRepository
from src.interface_adapters.controllers.order import OrderController
from src.infrastructure.boto.sns_connector import sns_arn, sns
from src.infrastructure.boto.sqs_connector import sqs_url, sqs

from src.use_cases.order.create.create_order import CreateOrderUseCase

from src.use_cases.order.delete.delete_order_dto import DeleteOrderOutputDto
from src.use_cases.order.find.find_order_dto import FindOrderOutputDto
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderOutputDto,
)
from src.use_cases.sns.sns import SNSUseCase
from src.use_cases.sqs.sqs import SQSUseCase


router = APIRouter()



@router.get("/", status_code=200, response_model=list[ListOrderOutputDto])
async def list_orders():
    try:
        return OrderController(OrderRepository()).list_orders()
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{order_uuid}/", status_code=200, response_model=FindOrderOutputDto)
async def retireve_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).retireve_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put(
    "/{order_uuid}/update-items/", status_code=200, response_model=UpdateOrderOutputDto
)
async def update_order_items(
    order_uuid: str,
    input_data: UpdateOrderItemsInputDto,
):
    try:
        return OrderController(OrderRepository()).update_order_items(
            order_uuid,
            input_data,
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put(
    "/{order_uuid}/progress-status/",
    status_code=200,
    response_model=UpdateOrderOutputDto,
)
async def progress_order_status(order_uuid: str):
    try:
        return OrderController(OrderRepository()).progress_order_status(
            order_uuid,
            SNSUseCase(
                sns,
                sns_arn,
            ),
        )
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{order_uuid}/", status_code=200, response_model=DeleteOrderOutputDto)
async def delete_order(order_uuid: str):
    try:
        return OrderController(OrderRepository()).delete_order(order_uuid)
    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.on_event("startup")
async def listen_create_queue():
    try:
        background_tasks = BackgroundTasks()
        sqs_usecase = SQSUseCase(sqs, sqs_url)
        background_tasks.add_task(sqs_usecase.sqs_listener, CreateOrderUseCase())

    except DomainException as err:
        raise HTTPException(
            status_code=status_code.HTTP_400_BAD_REQUEST,
            detail=err.message,
            headers={"WWW-Authenticate": "Bearer"},
        )