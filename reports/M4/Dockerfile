FROM continuumio/miniconda3
WORKDIR /home/baryan_edu/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

RUN pip install flask==1.1.1
RUN pip install flask_cors
RUN pip install werkzeug==1.0.0
RUN pip install opencv-python
RUN conda install pytorch==1.5.0 torchvision==0.6.0 cpuonly -c pytorch
RUN pip install numpy==1.18.1
RUN pip install urllib3
ADD backend .
RUN mkdir ./store
EXPOSE 8080
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv","python", "sapi.py"]
