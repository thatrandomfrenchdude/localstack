import boto3
from time import sleep
import os


class SQSClient():
    def __init__(self, q_url: str) -> None:
        self.queue_url = q_url
        self.client = self.config()

    def config(self) -> boto3.client:
        session = boto3.Session()
        return session.client(
            'sqs',
            region_name=os.environ.get('AWS_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=self.queue_url
        )

    def write2q(self, msg: str) -> None:
        try:
            self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=msg,
                DelaySeconds=0
            )
            print("Message posted to queue successfully")
        except Exception as e:
            print(f"Unable to post message to queue due to {e}")

    def readq(self) -> None:
        response = self.client.receive_message(
            QueueUrl=self.queue_url
        )
        if 'Messages' in response: 
            # get the message
            msg = response['Messages'][0]
            print(msg['Body'])
            # delete the message from the queue
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=msg['ReceiptHandle']
            )
        else:
            print("There are no messages in the queue")


if __name__ == '__main__':
    sqs = SQSClient("http://localhost:4566/000000000000/test")
    msg = "Hello, world!"
    sqs.write2q(msg)
    sleep(1)  # sleep for 15s to simulate delay
    sqs.readq()
