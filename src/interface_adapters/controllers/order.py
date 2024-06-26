from src.interface_adapters.gateways.authorization_microservice import (
    AuthorizationOutputDto,
)
from src.interface_adapters.gateways.interface.sns import SNSInterface
from src.interface_adapters.gateways.order_parser import CreateOrderParser
from src.interface_adapters.gateways.repositories.order import OrderRepositoryInterface
from src.use_cases.order.create.create_order import CreateOrderUseCase
from src.use_cases.order.create.create_order_dto import (
    CreateOrderInputDto,
    CreateOrderOutputDto,
)
from src.use_cases.order.delete.delete_order import DeleteOrderUseCase
from src.use_cases.order.delete.delete_order_dto import (
    DeleteOrderInputDto,
    DeleteOrderOutputDto,
)
from src.use_cases.order.find.find_order import FindOrderUseCase
from src.use_cases.order.find.find_order_dto import (
    FindOrderInputDto,
    FindOrderOutputDto,
)
from src.use_cases.order.list.list_order import ListOrderUseCase
from src.use_cases.order.list.list_order_dto import ListOrderOutputDto
from src.use_cases.order.update.update_order import UpdateOrderUseCase
from src.use_cases.order.update.update_order_dto import (
    UpdateOrderItemsInputDto,
    UpdateOrderOutputDto,
)


class OrderController:
    def __init__(self, repository: OrderRepositoryInterface):
        self.repository = repository

    def create_order(
        self,
        input_data: CreateOrderInputDto,
        create_order_parser: CreateOrderParser,
        current_user: AuthorizationOutputDto,
    ) -> CreateOrderOutputDto:
        create_use_case = CreateOrderUseCase(
            self.repository,
        )
        new_order = create_use_case.execute(
            create_order_parser.get_order_input_dto(input_data, current_user)
        )
        return new_order

    def list_orders(self) -> list[ListOrderOutputDto]:
        return ListOrderUseCase(self.repository).execute()

    def retireve_order(self, order_uuid: str) -> FindOrderOutputDto:
        find_use_case = FindOrderUseCase(self.repository)
        order = find_use_case.execute(FindOrderInputDto(uuid=order_uuid))
        return order

    def update_order_items(
        self,
        order_uuid: str,
        input_data: UpdateOrderItemsInputDto,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderUseCase(
            self.repository,
            FindOrderUseCase(self.repository),
        )
        order = update_use_case.update_order_items(order_uuid, input_data)
        return order

    def progress_order_status(
        self,
        order_uuid: str,
        sns_usecase: SNSInterface,
    ) -> UpdateOrderOutputDto:
        update_use_case = UpdateOrderUseCase(
            self.repository,
            FindOrderUseCase(self.repository),
        )
        order = update_use_case.progress_status(order_uuid, sns_usecase)
        return order

    def delete_order(self, order_uuid: str) -> DeleteOrderOutputDto:
        delete_use_case = DeleteOrderUseCase(self.repository)
        order = delete_use_case.execute(DeleteOrderInputDto(uuid=order_uuid))
        return order
