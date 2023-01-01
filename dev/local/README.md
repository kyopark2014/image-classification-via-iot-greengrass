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
2) [Deployment target] - [Target type]을 "Core device"를 설정하고, Target name으로 greengrass 설치시 사용한 이름을 아래처럼 입력합니다. 이후 [Next]선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/210171401-a8b07744-97fd-47b4-99a2-6f3bffd55252.png)

3) [Select components] - [Public components] 에서 아래와 같이 "aws.greengrass.Cli"와 "aws.greengrass.DLRImageClassification"을 선택합니다. 이후 나머지 설정은 기본값으로 하여 [Deploy]를 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/210171581-349197ee-95c5-4700-9425-06a6895257db.png)


### 4. 테스트 

동작을 확인하기 위하여 아래와 같이 

```java
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
cd image-classification-via-iot-greengrass/dev/local
```

