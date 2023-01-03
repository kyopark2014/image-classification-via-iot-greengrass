# IoT 디바이스에서 머신러닝을 이용한 이미지 분류하기

IoT 디바이스에서 이미지 분류를 위한 머신러닝을 활용하기 위해서는 효과적인 머신러닝 모델이 필요합니다. AWS에서 무료로 제공하는 [DLR 이미지 분류 모델 스토어](https://docs.aws.amazon.com/ko_kr/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)는 Greengrass가 설치된 디바이스에서 [ResNet-50 모델](https://viso.ai/deep-learning/resnet-residual-neural-network/)을 사용할 수 있도록 해줍니다. 

여기서는 [IoT Greengrass](https://github.com/kyopark2014/iot-greengrass)의 DLR model을 이용하여, IoT 디바이스에서 이미지 분류(Image Classification)를 쉽고 편리하게 이용하고자 합니다. 

DLR model을 활용하기 위해서 Built-in Component인 [DLR image classification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)을 제공하고 있습니다. 이것은 [variant.DLR.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)을 이용하여, 이미지 분류를 위한 머신러닝을 수행합니다.


## Built-in Component를 이용하는 방법

[DLR image classification](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)은 AWS에서 제공하는 public component로서 오픈 소스 프로젝트인 [DLR (Deep Learning Runtime)](https://github.com/neo-ai/neo-ai-dlr)을 베이스로 IoT 디바이스에서 이미지 분류를 추론(Inference)할 수 있도록 해줍니다. 

[Built-in Component](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/built-in-component.md)에서는 public component인 aws.greengrass.DLRImageClassification을 설치하고 사용하는 방법에 대해 설명하고 있습니다. 

사용자의 특정 목적에 따라 이미지 분류를 하려면, public component으로 어렵고, 아래와 같이 custom component를 생성하여 사용하여야 합니다. 


## Custom Component로 이용하는 방법

Custom component를 개발하는 과정은 [Local 환경에서 이미지 분류 추론 개발하기](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dev/local)와 [Script를 이용해 Component를 설치하여 이미지 분류 추론 개발하기](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dev/script)에서 상세하게 설명하고 있습니다. 

[Custom Component](https://github.com/kyopark2014/image-classification-via-iot-greengrass/blob/main/custom-component.md)에서는 DLR model을 이용하여 Component에서 추론(Inference)를 수행하는것을 설명합니다. 



### Greengrass Commands와 Memo

유용한 [Greengrass 명령어와 중요한 메모들](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-commands.md)를 정리하였습니다.


## Reference

[DLR image classification model store](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html)

[Github - DLR](https://github.com/neo-ai/neo-ai-dlr)

[Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)


[DLR: Compact Runtime for Machine Learning Models](https://neo-ai-dlr.readthedocs.io/en/latest/index.html)

[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano](https://github.com/daekeun-ml/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson)

