# Local에서 개발 구성

[DLR을 이용한 이미지 분류 추론](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dlr-inference)을 Cloud9으로 개발하는 과정을 설명합니다.

## 1) Greengrass 설치

[Cloud9으로 Greengrass 환경 설정](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9을 구성하고, Greengrass을 설치합니다. 편의상 Cloud9 생성시에 

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
