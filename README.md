# DLR Image Classification

Greengrass에서 Built-in Component를 이용하여 이미지 분류를 수행합니다. 

DLR image classification은 IoT Greengrass에서 제공하는 이미지 분류 Component로서 ResNet-50 모델을 사용합니다. 

"accessControl"을 보면 아래와 같이 "ml/dlr/image-classification" topic으로 IoT Core로 결과를 전송합니다. 

```java
{
   "aws.greengrass.ipc.mqttproxy": {
      "aws.greengrass.DLRImageClassification:mqttproxy:1": {
         "policyDescription": "Allows access to publish via topic ml/dlr/image-classification.",
         "operations": [
            "aws.greengrass#PublishToIoTCore"
         ],
         "resources": [
            "ml/dlr/image-classification"
         ]
      }
   }
}
```

## Configuration 

- "PublishResultsOnTopic": Inference 결과를 전달할 topic 이름입니다. 기본값은 "ml/dlr/image-classification" 입니다. 

- "Accelerator": CPU/GPU를 선택할 수 있습니다. 기본값은 cpu입니다. 

- "ImageDirectory": 이미지를 읽어오는 경로입니다. 

```java
/greengrass/v2/packages/artifacts-unarchived/component-name/image_classification/sample_images/
```

- "ImageName": 지원이미지 타입으로 jpeg, jpg, png, npy을 지원하고, 기본값은 jpeg 입니다. 

- "InferenceInterval": Inference를 수행하는 주기입니다. 기본값은 3600입니다.

- "UseCamera": 카메라 사용시 설정합니다. 기본값은 false 입니다.

로그는 아래와 같이 확인합니다. 

```java
sudo tail -f /greengrass/v2/logs/aws.greengrass.DLRImageClassification.log
```

## Workshop: Image Classification via Greengrass

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 아래와 같이 이미지에 대한 분류를 수행할 수 있습니다. 

아래와 같이 라이브러리를 설치합니다.

```java
sudo apt-get install libgl1 -y
```

"aws.greengrass.DLRImageClassification"을 배포할때 또는 배포후에 아래와 같이 config를 변경합니다.

```java
{
  "InferenceInterval": "60",
  "ImageDirectory": "/tmp/images/",
  "ImageName": "image.jpg"
}
```

성기의 config을 아래와 같이 "Configuration to merge"에 입력합니다. 

![noname](https://user-images.githubusercontent.com/52392004/204227376-1060ff56-2960-4814-a440-0984dd013715.png)


아래처럼 이미지를 업데이트 합니다.

```java
mkdir -p /tmp/images
wget "https://aws-iot-workshop-artifacts.s3.eu-west-1.amazonaws.com/packages/ggworkshop/image.jpg" -O /tmp/images/image.jpg
```

이후 결과를 IoT Core에서 확인합니다. 


## Reference

[DLR image classification model store](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)

[Github - DLR](https://github.com/neo-ai/neo-ai-dlr)

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)
