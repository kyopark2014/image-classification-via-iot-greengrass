# DLR Inference

DLR(Deep Learning Runtime) 이미지 분류 모델은 ResNet-50 모델을 Greengrass의 Artifact로 제공하는 머신러닝 모델입니다. 


## 라이브러리 설치

```java
sudo apt-get install libgl1 -y

pip3 install dlr 

pip3 install --upgrade pip
pip3 install scikit-build 
python3 -m pip install cmake pillow
pip3 install wheel
pip3 install gluoncv
```


## DLR 

[DLR Usage](https://github.com/neo-ai/neo-ai-dlr#usage)는 아래와 같습니다. 

```java
import dlr
import numpy as np

# Load model.
# /path/to/model is a directory containing the compiled model artifacts (.so, .params, .json)
model = dlr.DLRModel('/path/to/model', 'cpu', 0)

# Prepare some input data.
x = np.random.rand(1, 3, 224, 224)

# Run inference.
y = model.run(x)
```


## Reference 

[Github: neo-ai-dlr](https://github.com/neo-ai/neo-ai-dlr)
