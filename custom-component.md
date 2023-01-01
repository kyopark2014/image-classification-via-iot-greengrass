# Custom Component를 이용하여 IoT 디바이스에서 이미지 분류하기

[DLR을 이용한 이미지 분류 추론](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dlr-inference)에서는 DLR 모델이 정상적으로 분류를 할 수 있는지 Cloud9과 Container에서 확인하였습니다. 여기서에서는 이미지 분류 Container를 이용하여 IoT 디바이스에 Custom Component로 배포하는 동작을 설명합니다. 

## 1) Greengrass 설치

[Cloud9으로 Greengrass 환경 설정](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9을 구성하고, Greengrass을 설치합니다.

## 2) 필요한 라이브러리 설치

아래와 같이 DLR 구동에 필요한 라이브러리를 설치합니다. 

```java
sudo apt-get install libgl1 -y

pip3 install --upgrade pip
pip3 install scikit-build wheel 
pip3 install opencv-python==4.6.0.66 
pip3 install dlr

pip install dlr 
```

## 3) DLR image classification model store 설치

[variant.DLR.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html?icmpid=docs_gg_console)와 [aws.greengrass.Cli](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-cli-component.html?icmpid=docs_gg_console)을 설치합니다.


### 4) 테스트 

동작을 확인하기 위하여 아래와 같이 

```java
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
cd image-classification-via-iot-greengrass
```

[inference.py]()에서 아래의 경로를 확인합니다. 

```java
MODEL_DIR = '/greengrass/v2/packages/artifacts-unarchived/variant.DLR.ImageClassification.ModelStore/2.1.9/DLR-resnet50-x86_64-cpu-ImageClassification'
```

동작시험을 수행합니다.

```java
sudo python3 inference-test.py 
```

이때의 결과는 아래와 같습니다.
```java
MODEL_DIR: /greengrass/v2/packages/artifacts-unarchived/variant.DLR.ImageClassification.ModelStore/2.1.9/DLR-resnet50-x86_64-cpu-ImageClassification
IMAGE_DIR: /home/ubuntu/environment/image-classification-via-iot-greengrass/dlr-inference/images
cat.jpeg -> tabby, tabby cat
dog.jpg -> Weimaraner
macaw.jpg -> macaw
pelican.jpeg -> pelican
```


### Local component에서 조회하기 


[RequiresPrivilege](https://docs.aws.amazon.com/greengrass/v2/developerguide/component-recipe-reference.html)

(Optional) You can run the script with root privileges. If you set this option to true, then the AWS IoT Greengrass Core software runs this lifecycle script as root instead of as the system user that you configure to run this component. Defaults to false.
