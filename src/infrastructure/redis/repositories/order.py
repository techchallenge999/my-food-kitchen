from uuid import UUID


from src.domain.aggregates.order.value_objects.order_status import OrderStatus
from src.domain.shared.exceptions.order import OrderNotFoundException
from src.interface_adapters.gateways.repositories.order import (
    OrderItemRepositoryDto,
    OrderRepositoryDto,
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):
    def create(self, create_order_dto):
        pass

    def find(self, uuid):
        pass

    def list(self, filters={}, exclusive_filters={}):
        pass

    def update(self, update_order_dto):
       pass
    def delete(self, uuid):
        pass
