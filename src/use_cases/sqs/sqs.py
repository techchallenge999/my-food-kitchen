

import json
from src.interface_adapters.gateways.interface.sqs import SQSInterface

from src.use_cases.order.create.create_order import CreateOrderUseCase
from src.use_cases.order.create.create_order_dto import CreateOrderInputDto, CreateOrderItemInputDto



class SQSUseCase(SQSInterface):

    async def sqs_listener(self, create_order_usecase:CreateOrderUseCase):
        response = self.sqs_connector.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                message_body = json.loads(message['Body'])

                create_order_usecase.execute(
                    CreateOrderInputDto(
                        items=CreateOrderItemInputDto(
                            comment=message_body["comment"],
                            product_uuid=message_body["product_uuid"],
                            quantity=message_body["quantity"],
                        ),
                        user_uuid=message_body["user_uuid"],
                    )
                )

                self.sqs_connector.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
