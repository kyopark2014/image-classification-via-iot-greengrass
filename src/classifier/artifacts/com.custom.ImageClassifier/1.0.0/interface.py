import sys
import time
import traceback
import json

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    SubscriptionResponseMessage,
    UnauthorizedError,
    PublishMessage,
    BinaryMessage    
)

from classifier import classifier  

from logging import INFO, DEBUG, StreamHandler, getLogger
logger = getLogger()
logger.setLevel(INFO)

try:
    ipc_client = GreengrassCoreIPCClientV2()
except Exception:
    logger.error("Exception occurred: %s", file=sys.stderr)
    traceback.print_exc()
    exit(1)

topic = 'local/inference'

def main():    
    logger.debug("topic: {}".format(topic))

    try:
        # Subscription operations return a tuple with the response and the operation.
        _, operation = ipc_client.subscribe_to_topic(topic=topic, on_stream_event=on_stream_event,
            on_stream_error=on_stream_error, on_stream_closed=on_stream_closed)
        logger.debug("Successfully subscribed to topic: {}".format(topic))

        # Keep the main thread alive, or the process will exit.
        try:
            while True:
                time.sleep(10)
        except InterruptedError:
            logger.error("Subscribe interrupted.")

        # To stop subscribing, close the stream.
        operation.close()
    except UnauthorizedError:
        logger.error("Unauthorized error while subscribing to topic: %s", file=sys.stderr)      
        traceback.print_exc()
        exit(1)

def on_stream_event(event: SubscriptionResponseMessage) -> None:
    try:
        message = str(event.binary_message.message, 'utf-8')
        event_topic = event.binary_message.context.topic
        logger.info("Received new message on topic %s: %s", topic, message)      
        
        # Inference
        if event_topic == topic:
            json_data = json.loads(message) # json decoding        
            result = classifier(json_data)       
            logger.info("result: {}".format(result))

            # return the result to the consumer        
            publish_binary_message_to_topic(ipc_client, "local/result",  result)            

    except:
        traceback.print_exc()

def on_stream_error(error: Exception) -> bool:
    logger.error("Received a stream error: %s", file=sys.stderr)    
    traceback.print_exc()
    return False  # Return True to close stream, False to keep stream open.

def on_stream_closed() -> None:
    logger.error("Subscribe to topic stream closed.")

def publish_binary_message_to_topic(ipc_client, topic, message):
    binary_message = BinaryMessage(message=bytes(message, 'utf-8'))
    publish_message = PublishMessage(binary_message=binary_message)
    ipc_client.publish_to_topic(topic=topic, publish_message=publish_message)

if __name__ == '__main__':
    main()