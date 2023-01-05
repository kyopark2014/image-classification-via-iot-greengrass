# CDK로 Cloud9에서 이미지 분류 추론하기 

여기에서는 AWS의 개발환경인 Cloud9을 이용하여 Docker image된 ML 알고리즘을 IoT Greengrass에 배포하는 일련의 과정을 설명합니다. 

Cloud9은 브라우저만으로 코드를 작성, 실행 및 디버깅할 수 있는 클라우드 기반 IDE(통합 개발 환경)로서 Greengrass 디바이스 동작을 테스트하기에 유용합니다.

### 1) Cloud9 생성

[Cloud9 Console](https://ap-northeast-2.console.aws.amazon.com/cloud9control/home?region=ap-northeast-2#/create)에서 아래와 같이 [Name]을 입력합니다.

![noname](https://user-images.githubusercontent.com/52392004/204112727-f14df4fc-830f-4c58-b229-8adda848a7c0.png)

Platform은 "Ubuntu Server 18.04 LTS"을 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/210555080-8a171197-9428-434d-b75d-58af38994334.png)


아래로 이동하여 [Create]를 선택하면 수분후에 Cloud9이 생성됩니다.



## 2) Greengrass 설치하기 

Cloud9을 오픈하고 터미널을 실행합니다.

![noname](https://user-images.githubusercontent.com/52392004/204112636-de69a319-86d8-4199-91ff-1ff9fa1871b8.png)

아래와 같이 Greengrass를 다운로드 합니다. 

```java
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassCore
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
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
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


## 4) 배포 결과 확인

[Greengrass Console - Components](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components)에서 아래와 같이 생성된 component 정보를 확인합니다. 

![image](https://user-images.githubusercontent.com/52392004/210557261-5570543d-ffcc-42ea-85f4-468f115b735a.png)


[Greengrass Console - Deployment](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/deployments)에서 아래와 같이 배포상태를 확인합니다. 아래와 같이 Status가 "Completed"가 되어야 합니다. 

![image](https://user-images.githubusercontent.com/52392004/210557345-00686e44-d7fd-4670-9498-5b0f6a49cbf2.png)


아래와 같이 Inference API를 호출하는 local component인 "com.custom.requester"의 로그를 확인합니다.
```java
sudo tail -f /greengrass/v2/logs/com.custom.requester.log
```

로그에서 요청은 아래와 같이 "pelican.jpeg"를 입력으로 넣습니다. 

```java
{"image_dir": "/greengrass/v2/packages/artifacts/com.custom.requester/1.0.0", "fname": "pelican.jpeg"}
```

이때의 결과는 아래와 같이 "pelican"으로 정상적으로 분류가 되었습니다.

```java
2023-01-04T12:44:00.207Z [INFO] (Copier) com.custom.requester: stdout. Installing collected packages: awscrt, awsiotsdk. {scriptName=services.com.custom.requester.lifecycle.Install, serviceName=com.custom.requester, currentState=NEW}
2023-01-04T12:44:00.351Z [INFO] (Copier) com.custom.requester: stdout. Successfully installed awscrt-0.14.7 awsiotsdk-1.11.9. {scriptName=services.com.custom.requester.lifecycle.Install, serviceName=com.custom.requester, currentState=NEW}
2023-01-04T12:44:00.424Z [INFO] (pool-2-thread-25) com.custom.requester: shell-runner-start. {scriptName=services.com.custom.requester.lifecycle.Run, serviceName=com.custom.requester, currentState=STARTING, command=["python3 -u /greengrass/v2/packages/artifacts/com.custom.requester/1.0.0/reques..."]}
2023-01-04T12:44:00.532Z [INFO] (Copier) com.custom.requester: stdout. BASE_DIR =  /greengrass/v2/packages/artifacts/com.custom.requester/1.0.0. {scriptName=services.com.custom.requester.lifecycle.Run, serviceName=com.custom.requester, currentState=RUNNING}
2023-01-04T12:44:00.550Z [INFO] (Copier) com.custom.requester: stdout. Successfully subscribed to topic: local/result. {scriptName=services.com.custom.requester.lifecycle.Run, serviceName=com.custom.requester, currentState=RUNNING}
2023-01-04T12:44:50.618Z [INFO] (Copier) com.custom.requester: stdout. request: {"image_dir": "/greengrass/v2/packages/artifacts/com.custom.requester/1.0.0", "fname": "pelican.jpeg"}. {scriptName=services.com.custom.requester.lifecycle.Run, serviceName=com.custom.requester, currentState=RUNNING}
2023-01-04T12:44:51.225Z [INFO] (Copier) com.custom.requester: stdout. result: pelican. {scriptName=services.com.custom.requester.lifecycle.Run, serviceName=com.custom.requester, currentState=RUNNING}
```

실제 추론을 수행한 custom component인 "com.custom.ImageClassifier.log"은 로그는 아래와 같이 확인합니다. 

```java
 sudo tail -f /greengrass/v2/logs/com.custom.ImageClassifier.log
```

아래의 결과와 같이 "com.custom.requester"로 부터 요청을 받아서 추론을 통해 "pelican"이라는 결과를 얻고 있습니다. 

```java
2023-01-04T12:44:50.619Z [INFO] (Copier) com.custom.ImageClassifier: stdout. Received new message on topic local/inference: {"image_dir": "/greengrass/v2/packages/artifacts/com.custom.requester/1.0.0", "fname": "pelican.jpeg"}. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-04T12:44:51.223Z [INFO] (Copier) com.custom.ImageClassifier: stdout. result: pelican. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
```

## 5) 삭제

배포에 사용했던 S3의 Artifact와 IoT Greengrass에 있는 Component, Deployment는 아래 명령어를 통해 삭제할 수 있습니다. 

```java
cdk destroy --all
```

하지만 상기 명령어로 Device에 이미 배포된 Component들이 삭제되지 않습니다. 디바이스의 Component들은 Deployment에서 재배포시에 모든 Component를 리스트에서 제외하고 배포하여야 삭제가 가능합니다.




