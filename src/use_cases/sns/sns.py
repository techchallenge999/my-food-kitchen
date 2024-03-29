

import json
from typing import Dict
from fastapi import HTTPException

from src.interface_adapters.gateways.sns_interface import SNSInterface




class SNSUseCase(SNSInterface):
    def publish_message(self, message: Dict) -> Dict:
        response = self.sns_connector.publish(
            TopicArn=self.sns_topic_arn,
            Message=json.dumps(message)
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {"status": "success"}
        raise HTTPException(status_code=500, detail="Failed to publish event to SNS")
