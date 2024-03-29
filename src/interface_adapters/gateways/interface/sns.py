from abc import ABC, abstractmethod
from typing import Dict


class SNSInterface(ABC):
    def __init__(self, sns_connector, sns_topic_arn: str) -> None:
        self.sns_connector = sns_connector
        self.sns_topic_arn = sns_topic_arn

    @abstractmethod
    def publish_message(self, message: Dict):
        pass
