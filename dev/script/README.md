# Script를 이용해 Component를 설치하여 이미지 분류 추론 개발하기 

[DLR을 이용한 이미지 분류 추론](https://github.com/kyopark2014/image-classification-via-iot-greengrass/tree/main/dlr-inference)을 Cloud9으로 개발하는 과정을 설명합니다. 

## 1) Greengrass 설치

[Cloud9으로 Greengrass 환경 설정](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9을 구성하고, Greengrass을 설치합니다. 편의상 Cloud9 생성시에 Ubuntu 18.4을 선택합니다.

## 2. aws.greengrass.Cli 설치

[aws.greengrass.Cli](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-cli-component.html?icmpid=docs_gg_console)을 설치합니다.

1) [Deployment Console](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/deployments)에서 [Create]를 선택합니다.
2) [Deployment target] - [Target type]을 "Core device"를 설정하고, Target name으로 greengrass 설치시 사용한 이름을 아래처럼 입력합니다. 여기서는 "GreengrassCore-18163f7ac3e"으로 입력하고, [Next]선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/210171401-a8b07744-97fd-47b4-99a2-6f3bffd55252.png)

3) [Select components] - [Public components] 에서 아래와 같이 "aws.greengrass.Cli"을 선택합니다. 이후 나머지 설정은 기본값으로 하여 [Deploy]를 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/210172949-5f077172-63af-44c3-8e47-a11abb19bcfb.png)


## 2) Component를 설치하기 위하여 Script, Artifact, Receip을  다운로드

아래와 같이 github repository를 다운르드후 dev/script로 이동합니다. 

```java
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
cd image-classification-via-iot-greengrass/dev/script
```

"classfier.sh"을 실행합니다. 

```java
chmod a+x classifier.sh 
./classifier.sh 
```

실행하면 아래와 같은 로그르 확인할 수 있습니다.

```java
Jan 01, 2023 1:58:11 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jan 01, 2023 1:58:11 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: 1d37b8ac-af2d-49dc-98f5-47563295e54b
```

## 결과 확인하기 

아래와 같이 로그로 추론 결과를 확인할 수 있습니다. 

```java
sudo tail -f /greengrass/v2/logs/com.custom.ImageClassifier.log
```

이때의 결과는 아래와 같습니다. 

```java
2023-01-01T13:58:59.999Z [INFO] (Copier) com.custom.ImageClassifier: stdout. MODEL_DIR: /greengrass/v2/packages/artifacts-unarchived/variant.DLR.ImageClassification.ModelStore/2.1.9/DLR-resnet50-x86_64-cpu-ImageClassification. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.590Z [INFO] (Copier) com.custom.ImageClassifier: stdout. IMAGE_DIR: /greengrass/v2/packages/artifacts/com.custom.ImageClassifier/1.0.0/images. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.590Z [INFO] (Copier) com.custom.ImageClassifier: stdout. cat.jpeg -> tabby, tabby cat. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.590Z [INFO] (Copier) com.custom.ImageClassifier: stdout. dog.jpg -> Weimaraner. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.590Z [INFO] (Copier) com.custom.ImageClassifier: stdout. macaw.jpg -> macaw. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.590Z [INFO] (Copier) com.custom.ImageClassifier: stdout. pelican.jpeg -> pelican. {scriptName=services.com.custom.ImageClassifier.lifecycle.Run.Script, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
2023-01-01T13:59:02.642Z [INFO] (Copier) com.custom.ImageClassifier: Run script exited. {exitCode=0, serviceName=com.custom.ImageClassifier, currentState=RUNNING}
```


