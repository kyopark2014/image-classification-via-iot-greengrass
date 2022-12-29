# Built-in Component를 이용한 Image Classification

## AWS Built-in Component 

AWS의 이미지 분류를 위한 [IoT Greengrass Built-in Component](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-image-classification-component.html)는 추론(Inference) 결과를 "ml/dlr/image-classification"라는 topic으로 IoT Core로 전송합니다. 아래와 같이 Configuratio을 수정할 수 있습니다.

### Configuration 

- "PublishResultsOnTopic": Inference 결과를 전달할 topic 이름입니다. 기본값은 "ml/dlr/image-classification" 입니다. 

- "Accelerator": CPU/GPU를 선택할 수 있습니다. 기본값은 cpu입니다. 

- "ImageDirectory": 이미지를 읽어오는 경로입니다. 

```java
/greengrass/v2/packages/artifacts-unarchived/component-name/image_classification/sample_images/
```

- "ImageName": 지원이미지 타입으로 jpeg, jpg, png, npy을 지원하고, 기본값은 jpeg 입니다. 

- "InferenceInterval": Inference를 수행하는 주기입니다. 기본값은 3600입니다.

- "UseCamera": 카메라 사용시 설정합니다. 기본값은 false 입니다.

### 로그 확인 

로그는 아래와 같이 확인합니다. 

```java
sudo tail -f /greengrass/v2/logs/aws.greengrass.DLRImageClassification.log
```

## Cloud9으로 Greengrass 디바이스로 사용하기

### Cloud9 준비

[Cloud9을 Greengrass 디바이스로 사용하기](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9에 Greengrass를 설치합니다. 


### DLRImageClassification Component 설치하기 

#### 사전준비

아래와 같이 먼저 필요한 라이브러리를 Greengrass 디바이스에서 설치합니다.

```java
sudo apt-get install libgl1 -y
```

아래처럼 사용할 이미지를 다운로드하여 "/tmp/images/"에 저장합니다.

```java
mkdir -p /tmp/images
wget "https://aws-iot-workshop-artifacts.s3.eu-west-1.amazonaws.com/packages/ggworkshop/image.jpg" -O /tmp/images/image.jpg
```

아래처럼 github에서도 다운로드 가능합니다. 

```java
mkdir -p /tmp/images
wget https://raw.githubusercontent.com/kyopark2014/iot-greengrass-DLR-image-classification/main/image.jpg -O /tmp/images/image.jpg
```

#### Component 설치 

[Public Component Console](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/greengrass/v2/components/public)에서 아래와 같이 "aws.greengrass.DLRImageClassification"을 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/209589629-22d65571-da82-461d-81bf-ed2e5ed5d8fc.png)

이때 기본으로 설정된 recipe는 아래와 같습니다. 

```java
{
  "RecipeFormatVersion": "2020-01-25",
  "ComponentName": "aws.greengrass.DLRImageClassification",
  "ComponentVersion": "2.1.10",
  "ComponentType": "aws.greengrass.generic",
  "ComponentDescription": "Sample recipe - Image classification inference using DLR and resnet50 default model.",
  "ComponentPublisher": "AWS",
  "ComponentConfiguration": {
    "DefaultConfiguration": {
      "accessControl": {
        "aws.greengrass.ipc.mqttproxy": {
          "aws.greengrass.DLRImageClassification:mqttproxy:1": {
            "policyDescription": "Allows access to publish via topic ml/dlr/image-classification.",
            "operations": [
              "aws.greengrass#PublishToIoTCore"
            ],
            "resources": [
              "ml/dlr/image-classification"
            ]
          }
        }
      },
      "ImageName": "cat.jpeg",
      "InferenceInterval": "3600",
      "PublishResultsOnTopic": "ml/dlr/image-classification",
      "ModelResourceKey": {
        "armv7l": "DLR-resnet50-armv7l-cpu-ImageClassification",
        "aarch64": "DLR-resnet50-aarch64-cpu-ImageClassification",
        "x86_64": "DLR-resnet50-x86_64-cpu-ImageClassification",
        "windows": "DLR-resnet50-win-cpu-ImageClassification"
      }
    }
  },
  "ComponentDependencies": {
    "variant.DLR.ImageClassification.ModelStore": {
      "VersionRequirement": ">=2.1.0 <2.2.0",
      "DependencyType": "HARD"
    },
    "variant.DLR": {
      "VersionRequirement": ">=1.6.9 <1.7.0",
      "DependencyType": "HARD"
    },
    "aws.greengrass.Nucleus": {
      "VersionRequirement": ">=2.0.0 <2.10.0",
      "DependencyType": "SOFT"
    }
  },
  "Manifests": [
    {
      "Platform": {
        "os": "linux",
        "architecture": "arm"
      },
      "Lifecycle": {
        "setEnv": {
          "DLR_IC_MODEL_DIR": "{variant.DLR.ImageClassification.ModelStore:artifacts:decompressedPath}/{configuration:/ModelResourceKey/armv7l}",
          "DEFAULT_DLR_IC_IMAGE_DIR": "{artifacts:decompressedPath}/image_classification/sample_images/"
        },
        "run": {
          "RequiresPrivilege": "true",
          "script": "\n                                    . {variant.DLR:configuration:/MLRootPath}/greengrass_ml_dlr_venv/bin/activate\n                                    python3 {artifacts:decompressedPath}/image_classification/inference.py"
        }
      },
      "Artifacts": [
        {
          "Uri": "greengrass:gwGTP0uPD1KsqEEntRsLeg5qsSZSv6nDbwnigKNrXsY=/image_classification.zip",
          "Digest": "rozM+acRNzNGuUXokMX43EoAs6hMaw1tw2eQtiBqrEw=",
          "Algorithm": "SHA-256",
          "Unarchive": "ZIP",
          "Permission": {
            "Read": "OWNER",
            "Execute": "NONE"
          }
        }
      ]
    }
```    

오른쪽의 [Deploy]를 선택한후 [Create new deployment]를 선택합니다.

아래처럼 [Deployment target]에서 Greegrass device의 정보를 아래처럼 입력합니다. 이후 [Next]를 선택합니다.

![noname](https://user-images.githubusercontent.com/52392004/209589891-c2e4d67f-367c-4b86-8aeb-ea39a1c5f14f.png)

"aws.greengrass.DLRImageClassification"를 선택후, [Configuration component]를 선택합니다.

![noname](https://user-images.githubusercontent.com/52392004/209590283-5072ccd6-f89d-422d-956b-aa15dbcddeb4.png)

"Configuration to merge"에 아래와 같은 값을 입력하고, 아래로 스크롤하여 [Confirm]을 선택합니다. 

![noname](https://user-images.githubusercontent.com/52392004/204227376-1060ff56-2960-4814-a440-0984dd013715.png)

```java
{
  "InferenceInterval": "60",
  "ImageDirectory": "/tmp/images/",
  "ImageName": "image.jpg"
}
```

마찬가지로, "aws.greengrass.Cli"을 설치합니다. 

#### 결과확인

아래와 같이 Greengrass 디바이스에서 greengrass-cli을 이용하여, "aws.greengrass.DLRImageClassification"가 실행되고 있는지 확인합니다. 이때 "variant.DLR.ImageClassification.ModelStore" 등도 같이 설치됨을 알 수 있습니다. 

```java
$ sudo /greengrass/v2/bin/greengrass-cli component list
Dec 27, 2022 12:39:53 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Dec 27, 2022 12:39:53 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Components currently running in Greengrass:
Component Name: DeploymentService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: aws.greengrass.Nucleus
    Version: 2.9.2
    State: FINISHED
    Configuration: {"awsRegion":"ap-northeast-2","componentStoreMaxSizeBytes":"10000000000","deploymentPollingFrequencySeconds":"15","envStage":"prod","fleetStatus":{"periodicStatusPublishIntervalSeconds":86400.0},"greengrassDataPlaneEndpoint":"","greengrassDataPlanePort":"8443","httpClient":{},"iotCredEndpoint":"c198kakbg1m4dh.credentials.iot.ap-northeast-2.amazonaws.com","iotDataEndpoint":"anr3wll34rul5-ats.iot.ap-northeast-2.amazonaws.com","iotRoleAlias":"GreengrassV2TokenExchangeRoleAlias","jvmOptions":"-Dlog.store=FILE","logging":{},"mqtt":{"spooler":{}},"networkProxy":{"proxy":{}},"platformOverride":{},"runWithDefault":{"posixShell":"sh","posixUser":"ggc_user:ggc_group"},"telemetry":{}}
Component Name: variant.DLR.ImageClassification.ModelStore
    Version: 2.1.9
    State: FINISHED
    Configuration: {}
Component Name: aws.greengrass.Cli
    Version: 2.9.2
    State: RUNNING
    Configuration: {"AuthorizedPosixGroups":null,"AuthorizedWindowsGroups":null}
Component Name: FleetStatusService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: TelemetryAgent
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: UpdateSystemPolicyService
    Version: 0.0.0
    State: RUNNING
    Configuration: null
Component Name: variant.DLR
    Version: 1.6.11
    State: FINISHED
    Configuration: {"MLRootPath":"../variant.DLR/greengrass_ml","UseInstaller":"true","WindowsMLRootPath":"%cd%\\..\\variant.DLR\\greengrass_ml"}
Component Name: aws.greengrass.DLRImageClassification
    Version: 2.1.10
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"aws.greengrass.DLRImageClassification:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish via topic ml/dlr/image-classification.","resources":["ml/dlr/image-classification"]}}},"ImageDirectory":"/tmp/images/","ImageName":"image.jpg","InferenceInterval":"60","ModelResourceKey":{"aarch64":"DLR-resnet50-aarch64-cpu-ImageClassification","armv7l":"DLR-resnet50-armv7l-cpu-ImageClassification","windows":"DLR-resnet50-win-cpu-ImageClassification","x86_64":"DLR-resnet50-x86_64-cpu-ImageClassification"},"PublishResultsOnTopic":"ml/dlr/image-classification"}
```

아래 명령어로 로그로 동작상태를 확인할 수 있습니다. 

```java
$ sudo cat aws.greengrass.DLRImageClassification.log
2022-12-27T00:38:48.026Z [INFO] (Copier) aws.greengrass.DLRImageClassification: stdout. Using default camera: false. {scriptName=services.aws.greengrass.DLRImageClassification.lifecycle.run.script, serviceName=aws.greengrass.DLRImageClassification, currentState=RUNNING}
2022-12-27T00:38:48.442Z [INFO] (Copier) aws.greengrass.DLRImageClassification: stdout. {"timestamp": "2022-12-27 00:38:48.033218", "inference-type": "image-classification", "inference-description": "Top 5 predictions with score 0.3 or above ", "inference-results": [{"Label": "macaw", "Score": "9.598218"}, {"Label": "lorikeet", "Score": "6.3572783"}, {"Label": "black stork, Ciconia nigra", "Score": "4.962772"}, {"Label": "peacock", "Score": "4.6445074"}, {"Label": "jacamar", "Score": "4.5817575"}]}. {scriptName=services.aws.greengrass.DLRImageClassification.lifecycle.run.script, serviceName=aws.greengrass.DLRImageClassification, currentState=RUNNING}
2022-12-27T00:38:48.442Z [INFO] (Copier) aws.greengrass.DLRImageClassification: stdout. Publishing results to the IoT core.... {scriptName=services.aws.greengrass.DLRImageClassification.lifecycle.run.script, serviceName=aws.greengrass.DLRImageClassification, currentState=RUNNING}
```

이후 결과를 [MQTT test client](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test)에서 확인합니다. 

이때의 결과는 아래와 같습니다.

![image](https://user-images.githubusercontent.com/52392004/209591221-ee50e442-cc81-4fc3-b101-031b7ef0a860.png)


## Reference 

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)

