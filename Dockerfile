FROM ubuntu:16.04

RUN apt update && apt --yes --force-yes install wget unzip build-essential python python-dev virtualenv portaudio19-dev
RUN wget https://github.com/nxture/snowboy/archive/master.zip && unzip master.zip

RUN cd snowboy-master/ && \
    virtualenv -p python2 venv/snowboy && \
    . venv/snowboy/bin/activate && \
    cd examples/Python && \
    pip install -r requirements.txt

RUN apt -y remove wget unzip build-essential portaudio19-dev && apt -y autoremove && apt clean && rm -rf /var/lib/apt/lists/*

CMD cd snowboy-master/ && \
    . venv/snowboy/bin/activate && \
    cd examples/Python && \
    python generate_pmdl.py -rD=model -lang=en -n=hotword.pmdl