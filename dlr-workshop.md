# DLR Workshop: Image Classification via Greengrass

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 아래와 같이 이미지에 대한 분류를 수행할 수 있습니다. 

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
