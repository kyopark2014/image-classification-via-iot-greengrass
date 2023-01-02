import sys
import traceback
import time
import json
import os
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    SubscriptionResponseMessage,
    UnauthorizedError,
    PublishMessage,
    BinaryMessage
)

def main():
    topic = 'local/inference'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    print('BASE_DIR = ', BASE_DIR)

    try:
        ipc_client = GreengrassCoreIPCClientV2()

        # Subscription operations return a tuple with the response and the operation.
        _, operation = ipc_client.subscribe_to_topic(topic="local/result", on_stream_event=on_stream_event,
            on_stream_error=on_stream_error, on_stream_closed=on_stream_closed)
        print('Successfully subscribed to topic: ' + "local/result")
        
        try:
            while True: 
                message = {
                    'image_dir': '/greengrass/v2/packages/artifacts/com.custom.ImageClassifier/1.0.0/images',
                    'fname': 'cat.jpeg'
                }
                publish_binary_message_to_topic(ipc_client, topic,  json.dumps(message))
                print('request:', json.dumps(message))
                
                time.sleep(5)
        except InterruptedError:
            print('Publisher interrupted.')                

        # To stop subscribing, close the stream.
        operation.close()
    except UnauthorizedError:
        print('Unauthorized error while subscribing to topic: ' +
              topic, file=sys.stderr)
        traceback.print_exc()
        exit(1)
    
    except Exception:
        print('Exception occurred', file=sys.stderr)
        traceback.print_exc()
        exit(1)
    
def publish_binary_message_to_topic(ipc_client, topic, message):
    binary_message = BinaryMessage(message=bytes(message, 'utf-8'))
    publish_message = PublishMessage(binary_message=binary_message)
    ipc_client.publish_to_topic(topic=topic, publish_message=publish_message)

def on_stream_event(event: SubscriptionResponseMessage) -> None:
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('result: %s' % (message))

    except:
        traceback.print_exc()

def on_stream_error(error: Exception) -> bool:
    print('Received a stream error.', file=sys.stderr)
    traceback.print_exc()
    return False  # Return True to close stream, False to keep stream open.


def on_stream_closed() -> None:
    print('Subscribe to topic stream closed.')

if __name__ == '__main__':
    main()        