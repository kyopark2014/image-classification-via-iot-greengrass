# DLR Workshop: Image Classification via Greengrass

[Workshop - Image Classification via Greengrass](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter7-ml/10-step1)에 따라 아래와 같이 이미지에 대한 분류를 수행할 수 있습니다. 

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
