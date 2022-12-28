FROM amazon/aws-lambda-python:3.8

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip
RUN /var/lang/bin/python3.8 -m pip install joblib
RUN /var/lang/bin/python3.8 -m pip install scikit-learn
RUN /var/lang/bin/python3.8 -m pip install awsiotsdk pandas

#RUN sudo apt-get install libgl1 -y
RUN apt install libgl1 -y
RUN pip3 install dlr 
RUN pip3 install --upgrade pip
#RUN pip3 install scikit-build 
RUN python3 -m pip install cmake pillow
RUN pip3 install wheel
RUN pip3 install gluoncv

WORKDIR /var/task/dlr

COPY . .

#RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "/var/task/dlr/inference.py"]
