

import json
from src.interface_adapters.gateways.interface.sqs import SQSInterface

from src.use_cases.order.create.create_order import CreateOrderUseCase
from src.use_cases.order.create.create_order_dto import CreateOrderInputDto, CreateOrderItemInputDto



class SQSUseCase(SQSInterface):

    def sqs_listener(self, create_order_usecase:CreateOrderUseCase):
        print("*"*50)
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
                        items=[
                            CreateOrderItemInputDto(
                                comment=item["comment"],
                                product_uuid=item["product_uuid"],
                                quantity=item["quantity"],
                            ) for item in message_body["items"]
                        ],
                        total_amount=message_body.get("total_amount", 10),
                        user_uuid=message_body["user_uuid"],
                    )
                )

                self.sqs_connector.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
