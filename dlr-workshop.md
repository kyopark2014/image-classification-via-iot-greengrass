# DLR Workshop: Image Classification via Greengrass

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 아래와 같이 이미지에 대한 분류를 수행할 수 있습니다. 

## Cloud9을 Greengrass 디바이스로 사용하기

[Cloud9을 Greengrass 디바이스로 사용하기](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)에 따라 Cloud9에 Greengrass를 설치합니다. 


## DLRImageClassification Component 설치하기 

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

아래처럼,[Deployment target]에서 Greegrass device의 정보를 아래처럼 입력합니다. 이후 [Next]를 선택하여 deploy 합니다. 

![noname](https://user-images.githubusercontent.com/52392004/209589891-c2e4d67f-367c-4b86-8aeb-ea39a1c5f14f.png)





아래와 같이 라이브러리를 설치합니다.

```java
sudo apt-get install libgl1 -y
```

"aws.greengrass.DLRImageClassification"을 배포할때 또는 배포후에 아래와 같이 config를 변경합니다.

```java
{
  "InferenceInterval": "60",
  "ImageDirectory": "/tmp/images/",
  "ImageName": "image.jpg"
}
```

성기의 config을 아래와 같이 "Configuration to merge"에 입력합니다. 

![noname](https://user-images.githubusercontent.com/52392004/204227376-1060ff56-2960-4814-a440-0984dd013715.png)


아래처럼 이미지를 업데이트 합니다.

```java
mkdir -p /tmp/images
wget "https://aws-iot-workshop-artifacts.s3.eu-west-1.amazonaws.com/packages/ggworkshop/image.jpg" -O /tmp/images/image.jpg
```

이후 결과를 IoT Core에서 확인합니다. 

## Reference 

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)
