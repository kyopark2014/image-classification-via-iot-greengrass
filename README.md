# DLR Image Classification

여기에서는 IoT 디바이스에서 이미지 분류를 위한 머신러닝을 수행하는것에 대해 설명하고자 합니다. IoT Greengrass의 Component를 이용하면 쉽게 IoT 디바이스를 위한 어플리케이션을 개발하고, 편리하게 배포할 수 있습니다. 관련하여 AWS에서는 Built-in Component인 [DLR image classification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)을 제공하고 있으며, [variant.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)을 이용하여 이미지 분류를 위한 머신러닝을 수행할 수 있습니다. 하지만, public component는 사용자의 목적에 따라 수정이 어려우므로, DLR image classification을 private component로 구현할 수 있다면 여러용도로 편리하게 사용할 수 있습니다. 

IoT 디바이스에서 이미지 분류를 위한 머신러닝을 수행하는 2가지 방법에 대해 설명합니다.

## Built in component를 이용하는 방법

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

### Configuration 

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

[DLR Workshop](https://github.com/kyopark2014/iot-greengrass-DLR-image-classification/blob/main/dlr-workshop.md)에서는 Workshop에 대해 설명합니다. 



## Private component로 생성하여 활용하는 방법




### Greengrass Commands와 Memo

유용한 [Greengrass 명령어와 중요한 메모들](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-commands.md)를 정리하였습니다.


## Reference

[DLR image classification model store](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)

[Github - DLR](https://github.com/neo-ai/neo-ai-dlr)

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)


[DLR: Compact Runtime for Machine Learning Models](https://neo-ai-dlr.readthedocs.io/en/latest/index.html)

[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano](https://github.com/daekeun-ml/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson)
