# IoT 디바이스에서 머신러닝을 이용한 이미지 분류하기

IoT 디바이스에서 이미지 분류를 하기 위해서는 효과적인 머신러닝 모델이 필요합니다. AWS에서 무료로 제공하는 [DLR 이미지 분류 모델 스토어](https://docs.aws.amazon.com/ko_kr/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)를 이용하면, Greengrass가 설치된 디바이스에서 [ResNet-50 모델](https://viso.ai/deep-learning/resnet-residual-neural-network/)을 사용할 수 있습니다. [DLR (Deep Learning Runtime)](https://github.com/neo-ai/neo-ai-dlr) 이미지 분류 모델은 Built-in Component인 [variant.DLR.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)로 제공되며, 이것을 IoT device에서 활용하기 위해서는 또 다른 Built-in Component인 [aws.greengrass.DLRImageClassification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)을 이용하여 이미지 분류를 요청하거나, 별도의 Custom Component를 구현하여야 합니다. 


## Built-in Component를 이용한 이미지 분류 및 문제점

Greengrass에서 Built-in으로 제공하는 public component인 [aws.greengrass.DLRImageClassification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)은 IoT 디바이스에서 이미지 분류를 할 수 있도록 해줍니다. [[Built-in Component를 이용하여 IoT 디바이스에서 이미지 분류하기]](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/README.md)에서는 aws.greengrass.DLRImageClassification을 설치하고, 활용하는 방법에 대한 상세한 설명을 하고 있습니다. 

Public component인 aws.greengrass.DLRImageClassification을 이용하면, IoT 디바이스에서 손쉽게 이미지 분류를 구현할 수 있습니다. 하지만, 아래와 같이 주기(InferenceInterval), 이미지 로드하는 폴더(ImageDirectory), 이미지 이름(ImageName)만 설정할 수 있으며, 사용자의 목적에 따라 자유롭게 수정할 수 없습니다. 


```java
{
  "InferenceInterval": "60",
  "ImageDirectory": "/tmp/images/",
  "ImageName": "image.jpg"
}
```

또한, RESTful API처럼 Greengrass의 다른 Component에서 aws.greengrass.DLRImageClassification에 직접 요청을 보내고 결과를 얻는 방식이 아니라, IoT Core를 통해 결과를 확인하여야 합니다. 따라서, IoT 디바이스 만으로 로컬 컴포넌트에서 이미지 분류를 구현하고자 한다면 Custom Component에서 직접 [variant.DLR.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)의 DLR model을 로딩하여 활용할 수 있어야 합니다. 아래에서는 Custom component를 이용하여 variant.DLR.ImageClassification.ModelStore의 DLR model을 로드하고, 이미지 분류(Image Classification)를 쉽고 편리하게 수행하는것을 설명합니다. 


## Custom Component를 이용한 이미지 분류 

Edge에 있는 IoT 디바이스에서 이미지 분류를 수행하는 과정을 아래 Architecture에서 설명하고 있습니다. AWS Cloud의 Greengrass를 이용하여 디바이스에 Component를 배포하거나 관리할 수 있습니다. IoT 디바이스에 이미지 분류를 요청하는 component인 requester(com.custom.requester)와 추론을 수행하는 component인 classifier(com.custom.ImageClassifer)를 구현합니다. 두 Compoent는 [Nucleus](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html)를 통해 [IPC 통신](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html)을 수행합니다. 실제로 이미지 분류 추론을 수행하는 Inference modeule은 아래와 같이 Classifer와 DLR model(variant.DLR.ImageClassification.ModelStore)로 구성됩니다. 여기서, Requester는 "local/result" topic을 Subscribe 하여 결과를 얻고, Classifier는 "local/inference" toipc을 subscribe하여서 requester의 요청을 받아 들입니다. 


<img src="https://user-images.githubusercontent.com/52392004/211015785-45565ad7-cf7e-4314-b2c8-7f3ee76acca7.png" width="800">


Custom component를 개발하는 과정은 [Local 환경에서 이미지 분류 추론 개발하기](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dev/local)와 [Script를 이용해 Component를 설치하여 이미지 분류 추론 개발하기](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dev/script)에서 상세하게 설명하고 있습니다. 

이미비 분류를 수행하는 과정은 아래와 같습니다. 

1) Requester는 Greengrass의 local component로서 자신이 관리하는 이미지의 Path 및 파일명을 가지고 이미지 분류를 요청합니다. 

2) Nucleus의 local MQTT 역할을 이용하여, Requester는 "local/inference" topic으로 publish를 수행합니다. 

3) Classifier는 "local/inference"를 Subscribe하고 있다가, Requester가 보낸 이미지 분류 추론 요청을 받습니다.

4) Classifier는 DLR model로 추론(inference)을 수행합니다. 

5) DLR model은 이미지 분류 추론 결과를 Classifier에 전달합니다. 

6) Classifier는 "local/result" topic으로 결과를 전달합니다.

7) Requester는 "local/result" topic을 활용하여 이미지 분류 결과를 확인합니다. 



### Requester (com.custom.requester)

[com.custom.requester](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/requester/artifacts/com.custom.requester/1.0.0/requester.py)은 [Greengrass IPC Client V2](https://github.com/aws/aws-iot-device-sdk-python-v2)를 이용해 아래와 같이 "com.custom.ImageClassifer"로 추론 요청을 수행합니다. 

요청은 JSON 포맷으로된 메시지를 바이너리로 변환하여 publish 합니다. 
```python
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2

ipc_client = GreengrassCoreIPCClientV2()

message = {
  'image_dir': BASE_DIR,
  'fname': 'pelican.jpeg'
}
publish_binary_message_to_topic(ipc_client, topic,  json.dumps(message))

def publish_binary_message_to_topic(ipc_client, topic, message):
    binary_message = BinaryMessage(message=bytes(message, 'utf-8'))
    publish_message = PublishMessage(binary_message=binary_message)
    ipc_client.publish_to_topic(topic=topic, publish_message=publish_message)
```    

com.custom.ImageClassifier를 통해 추론을 수행한 결과는 "local/result" 토픽을 이용하여 아래처럼 확인합니다. 

```python
_, operation = ipc_client.subscribe_to_topic(topic="local/result", on_stream_event=on_stream_event,
  on_stream_error=on_stream_error, on_stream_closed=on_stream_closed)
            
def on_stream_event(event: SubscriptionResponseMessage) -> None:
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('result: %s' % (message))

    except:
        traceback.print_exc()
```        

[Pub/Sub IPC](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)를 이용해 edge에 설치된 component들 끼리 메시지를 교환하기 위해서는 [recipe](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/requester/recipes/com.custom.requester-1.0.0.json)을 아래와 같이 설정합니다. [aws.greengrass.ipc.pubsub](https://docs.aws.amazon.com/ko_kr/greengrass/v2/developerguide/ipc-publish-subscribe.html)은 디바이스의 local component들 사이에 메시지를 교환하기 위한 IPC 서비스 식별자입니다. 

```java
"ComponentConfiguration": {
    "DefaultConfiguration": {
      "accessControl": {
        "aws.greengrass.ipc.pubsub": {
          "com.custom.requester:pubsub:1": {
            "policyDescription": "Allows access to publish/subscribe to the topics.",
            "operations": [
              "aws.greengrass#PublishToTopic",
              "aws.greengrass#SubscribeToTopic"                  
            ],
            "resources": [
              "local/inference",
              "local/result"
            ]
          }
        }
      }
    }
  }
  ```

### Classifier (com.custom.ImageClassifier)

[interface.py](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/classifier/artifacts/com.custom.ImageClassifier/1.0.0/interface.py)에서는 "local/inference" 토픽으로 메시지를 받으면, classifier()로 요청합니다. 

```python
from classifier import classifier  

ipc_client = GreengrassCoreIPCClientV2()
topic = 'local/inference'

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
```

[classifier.py](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/classifier/artifacts/com.custom.ImageClassifier/1.0.0/classifier.py)는 아래와 같이 이미지를 로드하여 실제 추론을 수행하는 ["inference"](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/classifier/artifacts/com.custom.ImageClassifier/1.0.0/interface.py)의 handler()를 호출하고 결과가 오면, 가장 확률이 높은 결과를 리턴합니다. 

```python
from inference import handler  

def classifier(data):
    image_data = load_image(os.path.join(data['image_dir'], data['fname']))
    
    event = {
        'body': image_data
    }

    try:
        result = handler(event,"")          
        
        return result['body'][0]['Label']
```

[inference.py](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/classifier/artifacts/com.custom.ImageClassifier/1.0.0/inference.py)에서는 아래와 같이 기학습된 모델을 로딩하고 전달받은 이미지 데이터를 resize 한 후 추론을 수행합니다. 

```java
SCORE_THRESHOLD = 0.3
MAX_NO_OF_RESULTS = 5
SHAPE = (224, 224)

MODEL_DIR = '/greengrass/v2/packages/artifacts-unarchived/variant.DLR.ImageClassification.ModelStore/2.1.9/DLR-resnet50-x86_64-cpu-ImageClassification'

def load_model(model_dir):
    model = DLRModel(model_dir, dev_type='cpu', use_default_dlr=False)
    logger.debug('MODEL was loaded')
    return model

model = load_model(MODEL_DIR)

def handler(event, context):
    image_data = event['body']
    cvimage = resize(image_data, SHAPE)

    if cvimage is not None:
        result = predict_from_image(model, cvimage)
        return {
            'statusCode': 200,
            'body': result
        }  

def predict_from_image(model, image_data):
    result = []
    try:
        model_output = model.run(image_data)

        probabilities = model_output[0][0]
        sort_classes_by_probability = argsort(probabilities)[::-1]
        for i in sort_classes_by_probability[: MAX_NO_OF_RESULTS]:
            if probabilities[i] >= SCORE_THRESHOLD:
                result.append({"Label": str(synset[i]), "Score": str(probabilities[i])})
        
        return result
```

[recipes](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/src/classifier/recipes/com.custom.ImageClassifer-1.0.0.json)에서는 libgl1을 비롯한 라이브러리를 설치합니다.

```java
"Manifests": [{        
  "Lifecycle": {
    "Install": {
        "RequiresPrivilege": "true",
          "Script": "apt-get install libgl1 -y\n pip3 install --upgrade pip \n pip3 install scikit-build wheel opencv-python==4.6.0.66 dlr\n python -m pip install dlr\n pip3 install awsiotsdk"
    },
  "Run": {
    "RequiresPrivilege": "true",
    "Script": "python3 -u {artifacts:path}/interface.py"
  }
}
```

또한, 추론을 위한 라이브러리에 의존성(dependency)가 있으므로 아래와 같이 "ComponentDependencies"에서 "variant.DLR.ImageClassification.ModelStore"를 기술하여야 합니다. 

```java
      "ComponentDependencies": {
        "variant.DLR.ImageClassification.ModelStore": {
          "VersionRequirement": ">=2.1.0 <2.2.0",
          "DependencyType": "HARD"
        }
      }
```

### CDK를 이용한 Component 배포 준비

CDK를 이용하여 Component를 배포합니다. 

[cdk-greengrass-stack.ts](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/cdk-greengrass/lib/cdk-greengrass-stack.ts)에서는 s3 bucket을 생성하고, artifact를 복사한후 deployment를 이용해 배포합니다. 


```java
const s3Bucket = new s3.Bucket(this, "gg-depolyment-storage",{
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
  autoDeleteObjects: true,
  publicReadAccess: false,
});

// copy artifact into s3 bucket
new s3Deploy.BucketDeployment(this, "UploadArtifact", {
  sources: [s3Deploy.Source.asset("../src")],
  destinationBucket: s3Bucket,
}); 

new greengrassv2.CfnDeployment(this, 'MyCfnDeployment', {
  targetArn: `arn:aws:iot:ap-northeast-2:`+accountId+`:thing/`+deviceName,    
  components: {
    "com.custom.requester": {
      componentVersion: version_requester
    },
    "com.custom.ImageClassifier": {
      componentVersion: version_ImageClassifier
    },
    "aws.greengrass.Cli": {
      componentVersion: "2.9.2"
    }
  }
```


### 배포하기 

[CDK로 Cloud9에서 이미지 분류 추론하기](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/src)에서는 DLR model을 이용하여 Component에서 추론(Inference)를 수행하는것을 설명합니다. 


### Greengrass Commands와 Memo

유용한 [Greengrass 명령어와 중요한 메모들](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-commands.md)를 정리하였습니다.


## Reference

[DLR image classification model store](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)

[Github - DLR](https://github.com/neo-ai/neo-ai-dlr)

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)


[DLR: Compact Runtime for Machine Learning Models](https://neo-ai-dlr.readthedocs.io/en/latest/index.html)

[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano](https://github.com/daekeun-ml/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson)

