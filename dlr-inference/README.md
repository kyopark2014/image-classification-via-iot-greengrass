# DLR Inference

DLR(Deep Learning Runtime) 이미지 분류 모델은 ResNet-50 모델을 Greengrass의 Artifact로 제공하는 머신러닝 모델입니다. 


## 라이브러리 설치

아래와 같이 필요한 라이브러리를 설치합니다. 

```java
sudo apt-get install libgl1 -y

pip install dlr 

pip3 install --upgrade pip
pip3 install scikit-build 
python3 -m pip install cmake pillow
pip3 install wheel
pip3 install gluoncv

pip3 install opencv-python
```

## 실행 

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

## Reference 

[Github: neo-ai-dlr](https://github.com/neo-ai/neo-ai-dlr)
