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
    python generate_pmdl.py -r1=model/record1.wav -r2=model/record2.wav -r3=model/record3.wav -r4=model/record4.wav -r5=model/record5.wav -r6=model/record6.wav -r7=model/record7.wav -r8=model/record8.wav -r9=model/record9.wav -r10=model/record10.wav -lang=en -n=model/hotword.pmdl
