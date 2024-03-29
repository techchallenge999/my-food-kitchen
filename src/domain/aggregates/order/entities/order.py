from uuid import UUID

from src.domain.aggregates.order.interfaces.order import (
    OrderInterface,
    OrderItemInterface,
)
from src.domain.aggregates.order.validators.order import OrderValidator
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface


class Order(OrderInterface):
    def __init__(
        self,
        items: list[OrderItemInterface],
        order_repository: OrderRepositoryInterface,
        total_amount:str,
        uuid: UUID,
        status: OrderStatus = OrderStatus.PENDING_PAYMENT,
        user_uuid: UUID | None = None,
    ):
        self._items = items
        self._status = status
        self._total_amount = total_amount
        self._user_uuid = user_uuid
        self._uuid = uuid
        self._validator = OrderValidator(
            self, order_repository
        )
        self.validator.validate()

    @property
    def items(self):
        return self._items

    @property
    def status(self):
        return self._status

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def user_uuid(self):
        if isinstance(self._user_uuid, UUID):
            return str(self._user_uuid)
        return None

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def validator(self):
        return self._validator

