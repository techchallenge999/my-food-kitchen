from abc import ABC, abstractmethod


class SQSInterface(ABC):
    def __init__(self, sqs_connector, queue_url: str) -> None:
        self.sqs_connector = sqs_connector
        self.queue_url = queue_url

    @abstractmethod
    def sqs_listener(self):
        pass
