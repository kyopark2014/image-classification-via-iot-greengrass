# Local에서 개발 구성

[DLR을 이용한 이미지 분류 추론](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dlr-inference)을 Cloud9으로 개발하는 과정을 설명합니다.

## 1) Greengrass 설치

[Cloud9으로 Greengrass 환경 설정](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9을 구성하고, Greengrass을 설치합니다. 편의상 Cloud9 생성시에 Ubuntu 18.4을 선택합니다.

## 2) 필요한 라이브러리 설치

Ubuntu 18.4에 맞게 아래와 같이 DLR 구동에 필요한 라이브러리를 설치합니다. 

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
