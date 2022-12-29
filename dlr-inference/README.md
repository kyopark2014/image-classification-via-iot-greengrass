# DLR을 이용한 이미지 분류 추론

[DLR(Deep Learning Runtime)](https://docs.aws.amazon.com/greengrass/v2/developerguide/dlr-component.html) 이미지 분류 모델은 ResNet-50 모델을 Greengrass의 Artifact로 제공하는 머신러닝 모델입니다. 

## 라이브러리 설치

### Ubuntu 18.4

Ubuntu인 경우에 아래와 같은 라이브러리를 설치합니다. OpenCV은 gluoncv 또는 opencv-python을 설치하면 됩니다.

```java
sudo apt-get install libgl1 -y

pip3 install --upgrade pip
pip3 install scikit-build wheel gluoncv dlr

pip install dlr 
```

### Amazon Linux 2

Amazon Linux인 경우에 아래와 같이 필요한 라이브러리를 설치합니다. 

```java
# sudo yum update
sudo yum install libglvnd-glx -y

pip3 install --upgrade pip
pip3 install scikit-build wheel gluoncv dlr

sudo pip install dlr
```

## 실행 

```java
git clone https://github.com/kyopark2014/image-classification-via-iot-greengrass
cd image-classification-via-iot-greengrass/dlr-inference/
```

아래와 같이 실행합니다. 

```java
python3 inference.py 
```

여기서는 아래와 같은 "cat.jpeg"을 사용하였고 이때의 결과는 아래와 같습니다. 

```java
result: {'Label': 'tabby, tabby cat', 'Score': '7.7391315'}
result: {'Label': 'Egyptian cat', 'Score': '6.956063'}
result: {'Label': 'tiger cat', 'Score': '6.775721'}
result: {'Label': 'doormat, welcome mat', 'Score': '5.3863106'}
result: {'Label': 'plastic bag', 'Score': '4.5193176'}
```

사용한 이미지는 아래와 같습니다.

<img src="https://user-images.githubusercontent.com/52392004/209852850-4f3792e8-2423-4689-83ed-3b98881616d7.png" width="400">

## Container

## Basic Docker Commends

Docker 소스로 이미지를 빌드합니다. 

```java
docker build -t dlr:v1 .
```

빌드된 이미지를 확인합니다. 

```java
docker images
```

Docker를 실행합니다. 

```java
docker run -d -p 8080:8080 dlr:v1
```


Docker의 실행된 container 정보를 확인합니다. 

```java
docker ps

CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
41e297948511   dlr:v1   "/lambda-entrypoint.…"   6 seconds ago   Up 4 seconds   0.0.0.0:8080->8080/tcp   stupefied_carson
```

Bash shell로 접속합니다.

```java
docker exec -it  41e297948511 /bin/bash
```





## Reference 

[Github: neo-ai-dlr](https://github.com/neo-ai/neo-ai-dlr)
