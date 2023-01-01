# Local 환경에서 이미지 분류 추론 개발하기 

[DLR을 이용한 이미지 분류 추론](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dlr-inference)을 Cloud9으로 개발하는 과정을 설명합니다. 

## 1. Greengrass 설치

[Cloud9으로 Greengrass 환경 설정](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9을 구성하고, Greengrass을 설치합니다. 편의상 Cloud9 생성시에 Ubuntu 18.4을 선택합니다.

## 2. 필요한 라이브러리 설치

Ubuntu 18.4에 맞게 아래와 같이 DLR 구동에 필요한 라이브러리를 설치합니다.
 
libgl1은 root 권한으로 apt-get으로 설치합니다.

```java
sudo apt-get install libgl1 -y
```

python 라이브러리를 아래처럼 설치합니다. 

```java
pip3 install --upgrade pip
pip3 install scikit-build wheel 
pip3 install opencv-python==4.6.0.66 
pip3 install dlr

pip install dlr 
```

## 3. DLR image classification model store 설치

[variant.DLR.ImageClassification.ModelStore](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-model-store-component.html?icmpid=docs_gg_console)와 [aws.greengrass.Cli](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-cli-component.html?icmpid=docs_gg_console)을 설치합니다.

1) [Deployment Console](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/deployments)에서 [Create]를 선택합니다.
2) [Deployment target] - [Target type]을 "Core device"를 설정하고, Target name으로 greengrass 설치시 사용한 이름을 아래처럼 입력합니다. 여기서는 "GreengrassCore-18163f7ac3e"으로 입력하고, [Next]선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/210171401-a8b07744-97fd-47b4-99a2-6f3bffd55252.png)

3) [Select components] - [Public components] 에서 아래와 같이 "aws.greengrass.Cli"와 "variant.DLR.ImageClassification.ModelStore"을 선택합니다. 이후 나머지 설정은 기본값으로 하여 [Deploy]를 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/210172225-586dfc6d-a4e6-48cc-a842-f14d14d3ca02.png)


### 4. 테스트 

동작을 확인하기 위하여 아래와 같이 코드를 다운로드 하고 소스 코드 위치로 이동합니다.

```java
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
cd image-classification-via-iot-greengrass/dev/local
```

이미지 분류 모델은 "variant.DLR.ImageClassification.ModelStore"으로 부터 가져오므로 아래와 같이 root 권한으로 실행합니다. 

```java
sudo python3 inference-test.py 
```

이때의 결과는 아래와 같습니다. 

```java
MODEL_DIR: /greengrass/v2/packages/artifacts-unarchived/variant.DLR.ImageClassification.ModelStore/2.1.9/DLR-resnet50-x86_64-cpu-ImageClassification
IMAGE_DIR: /home/ubuntu/environment/image-classification-via-iot-greengrass/dev/local/images
cat.jpeg -> tabby, tabby cat
dog.jpg -> Weimaraner
macaw.jpg -> macaw
pelican.jpeg -> pelican
```
