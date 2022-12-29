# IoT 디바이스에서 머신러닝을 이용한 이미지 분류하기

머신러닝 알고리즘을 이용하여 IoT 디바이스에서 이미지 분류를 수행하고자 합니다. [IoT Greengrass](https://github.com/kyopark2014/iot-greengrass)의 Component를 이용하면 쉽게 IoT 디바이스를 위한 어플리케이션을 개발하고, 편리하게 배포할 수 있습니다. 관련하여 AWS에서는 Built-in Component인 [DLR image classification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)을 제공하고 있으며, [variant.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)을 이용하여 이미지 분류를 위한 머신러닝을 수행할 수 있습니다. 하지만, public component는 사용자의 목적에 따라 수정이 어려우므로, DLR image classification을 custom component로 구현하는것도 설명합니다. 

아래와 같이 머신러닝을 이용하여 IoT 디바이스에서 이미지 분류를 수행하는 2가지 방법에 대해 설명합니다. 여기서 머신러닝 모델은 [ResNet-50 모델](https://viso.ai/deep-learning/resnet-residual-neural-network/)을 이용하는 [DLR (Deep Learning Runtime)](https://github.com/neo-ai/neo-ai-dlr)을 활용합니다. 

## Built-in Component를 이용하는 방법

[Built-in Component](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/built-in-component.md)에서는 AWS에서 제공하는 Component로 이미지 분류를 제공하는것을 보여줍니다. 


## Custom Component로 이용하는 방법

[Custom Component](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/custom-component.md)에서는 DLR model을 이용하여 Component에서 추론(Inference)를 수행하는것을 설명합니다. 

## RESNET-50 examples

- [GluonCV ResNet50 Classifier Demo](https://aws.amazon.com/marketplace/ai/model-evaluation?productId=587dc453-b6d6-487e-abc4-133b4bd3a0ed)

- [RESNET-50 Demo](https://aws.amazon.com/marketplace/ai/model-evaluation?productId=cc879d3b-e759-4270-9afb-ceb50d2f7fe6)

 

### Greengrass Commands와 Memo

유용한 [Greengrass 명령어와 중요한 메모들](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-commands.md)를 정리하였습니다.


## Reference

[DLR image classification model store](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)

[Github - DLR](https://github.com/neo-ai/neo-ai-dlr)

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)


[DLR: Compact Runtime for Machine Learning Models](https://neo-ai-dlr.readthedocs.io/en/latest/index.html)

[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano](https://github.com/daekeun-ml/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson)

