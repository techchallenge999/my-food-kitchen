from dataclasses import asdict
from uuid import UUID
import json


from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.infrastructure.redis.database import get_redis_db
from src.interface_adapters.gateways.repositories.order import (
    OrderRepositoryDto,
    OrderItemRepositoryDto,
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):
    def create(self, create_order_dto):
        db = get_redis_db()
        db.set(create_order_dto.uuid, json.dumps(asdict(create_order_dto)))

    def find(self, uuid):
        db = get_redis_db()
        order_as_string = db.get(uuid)
        if not order_as_string:
            raise OrderNotFoundException("Oder not found")
        order = json.loads(order_as_string)
        return OrderRepositoryDto(
            items=[
                OrderItemRepositoryDto(
                    comment=item["comment"],
                    product_uuid=str(item["product"]["uuid"]),
                    quantity=item["quantity"],
                )
                for item in order["items"]
            ],
            status=order["status"],
            total_amount=order["total_amount"],
            uuid=str(order["uuid"]),
            user_uuid=str(order["user_uuid"]) if order["user_uuid"] else None,
            created_at=order["created_at"],
            updated_at=order["updated_at"],
        )

    def list(self):
        db = get_redis_db()
        keys = db.keys('*')
        orders = map(lambda order: json.loads(order), db.mget(keys))

        return [
            OrderRepositoryDto(
                items=[
                    OrderItemRepositoryDto(
                        comment=item["comment"],
                        product_uuid=str(item["product"]["uuid"]),
                        quantity=item["quantity"],
                    )
                    for item in order["items"]
                ],
                status=order["status"],
                total_amount=order["total_amount"],
                uuid=str(order["uuid"]),
                user_uuid=str(order["user_uuid"]),
                created_at=order["created_at"],
                updated_at=order["updated_at"],
            )
            for order in orders
        ]

    def update(self, update_order_dto):
        db = get_redis_db()
        order_as_string = db.get(update_order_dto.uuid)
        if not order_as_string:
            raise OrderNotFoundException("Oder not found")
        db.set(update_order_dto.uuid, json.dumps(asdict(update_order_dto)))


    def delete(self, uuid):
        db = get_redis_db()
        db.delete(uuid)
