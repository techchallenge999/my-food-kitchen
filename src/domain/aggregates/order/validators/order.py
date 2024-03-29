from uuid import UUID

from src.domain.aggregates.order.interfaces.order import OrderInterface
from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.exceptions.base import InvalidUUIDException
from src.domain.shared.exceptions.order import InvalidOrderStatusException
from src.domain.shared.interfaces.validator import ValidatorInterface


class OrderValidator(ValidatorInterface):
    def __init__(
        self,
        domain_object: OrderInterface,
    ):
        self._order = domain_object

    def validate(self):
        self._raise_if_invalid_order_status()
        self._raise_if_invalid_uuid()

    def _raise_if_invalid_order_status(self) -> None:
        if self._is_invalid_order_status():
            raise InvalidOrderStatusException()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _is_invalid_order_status(self) -> bool:
        return not isinstance(self._order.status, OrderStatus)

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._order.uuid), UUID)
        except ValueError:
            return True
