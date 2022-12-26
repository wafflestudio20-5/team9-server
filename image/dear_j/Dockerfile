FROM public.ecr.aws/docker/library/python:3.8.16

COPY ./dear_j /var/dear_j
COPY ./requirements.txt /var/requirements.txt
COPY ./run_interface.sh /var/run_interface.sh

RUN python3 -m pip install --upgrade pip 
RUN pip3 install -r /var/requirements.txt

WORKDIR /var

ENTRYPOINT [ "./run_interface.sh" ]
