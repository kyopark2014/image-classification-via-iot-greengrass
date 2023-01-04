# CDK로 Cloud9에서 이미지 분류 추론하기 

여기에서는 AWS의 개발환경인 Cloud9을 이용하여 Docker image된 ML 알고리즘을 IoT Greengrass에 배포하는 일련의 과정을 설명합니다. 

## 1) Cloud9을 Greengrass 디바이스로 사용하기

Cloud9은 브라우저만으로 코드를 작성, 실행 및 디버깅할 수 있는 클라우드 기반 IDE(통합 개발 환경)로서 Greengrass 디바이스 동작을 테스트하기에 유용합니다.

### Cloud9 생성

[Cloud9 Console](https://ap-northeast-2.console.aws.amazon.com/cloud9control/home?region=ap-northeast-2#/create)에서 아래와 같이 [Name]을 입력합니다.

![noname](https://user-images.githubusercontent.com/52392004/204112727-f14df4fc-830f-4c58-b229-8adda848a7c0.png)

[Instance type]은 어떤 type이라도 관련없으나 여기서는 편의상 m5.large를 선택하였습니다. Platform은 "Ubuntu Server 18.04 LTS"을 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/204112516-ebd04eb3-e1a5-4a87-8bab-8782ecd511ae.png)

아래로 이동하여 [Create]를 선택하면 수분후에 Cloud9이 생성됩니다.

## 2) Greengrass 설치하기 

### Greengrass installer 다운로드

Cloud9을 오픈하고 터미널을 실행합니다.

![noname](https://user-images.githubusercontent.com/52392004/204112636-de69a319-86d8-4199-91ff-1ff9fa1871b8.png)

아래와 같이 Greengrass를 다운로드 합니다. 

```java
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

### Greengrass 설치 

아래와 같이 디바이스 이름은 "GreengrassCore-18163f7ac3e", Group은 ggc_user:ggc_group로 설치를 진행합니다. 

```java
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
	--aws-region ap-northeast-2 \
	--thing-name GreengrassCore-18163f7ac3e \
	--thing-group-name GreengrassGroup \
	--component-default-user ggc_user:ggc_group \
	--provision true \
	--setup-system-service true \
	--deploy-dev-tools true
```

설치가 다 완료가 되면, [Greengrass Console](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/cores)에서 아래와 같이 Greengrass core device로 "GreengrassCore-18163f7ac3e"가 등록된것을 알 수 있습니다. 설치후 Console 화면에 Core device 정보가 노출되는데 수분정도 지연될수 있으니 보이지 않는 경우에 몇분 후에 refresh 합니다. 

![noname](https://user-images.githubusercontent.com/52392004/204112707-7d82e8dd-4e30-4c24-9e77-c64f42995a76.png)


### Cloud9의 EBS 크기 변경 

필요시 [EBS 크기 변경](https://github.com/kyopark2014/technical-summary/blob/main/resize.md)에 따라 EBS 크기를 확대합니다. 다수의 Docker 이미지 빌드시 Cloud9의 기본 사용용량이 부족할 수 있습니다. 

## 3) CDK Deployment

여기에서는 CDK를 이용해 머신러닝 알고리즘 추론을 IoT Greengrass에 배포하는 방법에 대해 설명합니다. 

### Github Code를 활용하는 경우

아래와 같이 github의 코드를 다운로드 합니다. 

```java
https://github.com/kyopark2014/image-classification-via-iot-greengrass
```

cdk 폴더로 이동하여 필요한 라이브러리를 설치합니다. "aws-cdk-lib"는 CDK V2이고, "Path"는 Docker image 생성시 필요한 라이브러리입니다. 

```java
cd image-classification-via-iot-greengrass/cdk-greengrass/
npm install aws-cdk-lib
```


Component들이 여러개의 stack으로 구성하였으므로 아래와 같이 배포를 수행합니다. 

```java
cdk deploy --all
```


## 배포 결과 확인

[Greengrass Console - Components](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components)에서 아래와 같이 생성된 component 정보를 확인합니다. 

![image](https://user-images.githubusercontent.com/52392004/204181933-402f5f40-7048-4e3f-9d9e-120e1a0a42a2.png)


[Greengrass Console - Deployment](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/deployments)에서 아래와 같이 배포상태를 확인합니다. 아래와 같이 Status가 "Completed"가 되어야 합니다. 

![image](https://user-images.githubusercontent.com/52392004/204182044-8a55bae4-c5fc-49ee-9d98-d6b9006610b3.png)


아래와 같이 Inference API를 호출하는 local component인 "com.ml.consumer"의 로그를 확인합니다.
```java
sudo tail -f /greengrass/v2/logs/com.ml.consumer.log
```

로그에서 요청은 아래와 같습니다. 

```java
2022-11-28T03:00:34.872Z [INFO] (Copier) com.ml.consumer: stdout. request: {"body": "[{\"fixed acidity\":6.6,\"volatile acidity\":0.24,\"citric acid\":0.28,\"residual sugar\":1.8,\"chlorides\":0.028,\"free sulfur dioxide\":39,\"total sulfur dioxide\":132,\"density\":0.99182,\"pH\":3.34,\"sulphates\":0.46,\"alcohol\":11.4,\"color_red\":0,\"color_white\":1},{\"fixed acidity\":8.7,\"volatile acidity\":0.78,\"citric acid\":0.51,\"residual sugar\":1.7,\"chlorides\":0.415,\"free sulfur dioxide\":12,\"total sulfur dioxide\":66,\"density\":0.99623,\"pH\":3.0,\"sulphates\":1.17,\"alcohol\":9.2,\"color_red\":1,\"color_white\":0}]", "isBase64Encoded": false}. {scriptName=services.com.ml.consumer.lifecycle.Run, serviceName=com.ml.consumer, currentState=RUNNING}
```

이때의 결과는 로그에서 아래처럼 확인할 수 있습니다. 
```java
2022-11-28T03:00:34.896Z [INFO] (Copier) com.ml.consumer: stdout. result: [6.573914051055908, 4.869720935821533]. {scriptName=services.com.ml.consumer.lifecycle.Run, serviceName=com.ml.consumer, currentState=RUNNING}
```

container component인 "com.ml.xgboost"의 로그는 아래와 같습니다. 

```java
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. Received new message on topic local/inference: {"body": "[{\"fixed acidity\":6.6,\"volatile acidity\":0.24,\"citric acid\":0.28,\"residual sugar\":1.8,\"chlorides\":0.028,\"free sulfur dioxide\":39,\"total sulfur dioxide\":132,\"density\":0.99182,\"pH\":3.34,\"sulphates\":0.46,\"alcohol\":11.4,\"color_red\":0,\"color_white\":1},{\"fixed acidity\":8.7,\"volatile acidity\":0.78,\"citric acid\":0.51,\"residual sugar\":1.7,\"chlorides\":0.415,\"free sulfur dioxide\":12,\"total sulfur dioxide\":66,\"density\":0.99623,\"pH\":3.0,\"sulphates\":1.17,\"alcohol\":9.2,\"color_red\":1,\"color_white\":0}]", "isBase64Encoded": false}. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. event:  {'body': '[{"fixed acidity":6.6,"volatile acidity":0.24,"citric acid":0.28,"residual sugar":1.8,"chlorides":0.028,"free sulfur dioxide":39,"total sulfur dioxide":132,"density":0.99182,"pH":3.34,"sulphates":0.46,"alcohol":11.4,"color_red":0,"color_white":1},{"fixed acidity":8.7,"volatile acidity":0.78,"citric acid":0.51,"residual sugar":1.7,"chlorides":0.415,"free sulfur dioxide":12,"total sulfur dioxide":66,"density":0.99623,"pH":3.0,"sulphates":1.17,"alcohol":9.2,"color_red":1,"color_white":0}]', 'isBase64Encoded': False}. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. isBase64Encoded:  False. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. Base64 decoding is not required. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. body:  [{"fixed acidity":6.6,"volatile acidity":0.24,"citric acid":0.28,"residual sugar":1.8,"chlorides":0.028,"free sulfur dioxide":39,"total sulfur dioxide":132,"density":0.99182,"pH":3.34,"sulphates":0.46,"alcohol":11.4,"color_red":0,"color_white":1},{"fixed acidity":8.7,"volatile acidity":0.78,"citric acid":0.51,"residual sugar":1.7,"chlorides":0.415,"free sulfur dioxide":12,"total sulfur dioxide":66,"density":0.99623,"pH":3.0,"sulphates":1.17,"alcohol":9.2,"color_red":1,"color_white":0}]. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. values:     fixed acidity  volatile acidity  ...  color_red  color_white. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. 0            6.6              0.24  ...          0            1. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. 1            8.7              0.78  ...          1            0. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. [2 rows x 13 columns]. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. result: [6.573914 4.869721]. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
2022-11-28T03:07:05.358Z [INFO] (Copier) com.ml.xgboost: stdout. result: [6.573914051055908, 4.869720935821533]. {scriptName=services.com.ml.xgboost.lifecycle.Run, serviceName=com.ml.xgboost, currentState=RUNNING}
```

## 삭제


배포에 사용했던 S3와 Recipe, Artifact의 삭제는 아래 명령어를 통해 삭제할 수 있습니다. 하지만 아래 명령어로 Device에 배포된 Component들이 삭제되지 않습니다. 디바이스의 Component들은 재배포시 해당 Component를 리스트에서 제외하고 배포하여야 삭제가 가능합니다.

```java
cdk destroy --all
```




