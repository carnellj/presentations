FROM python:3.6

RUN mkdir -p /usr/local/bin/simple-contact/
COPY requirements.txt /usr/local/bin/simple-contact/.
COPY simple-contact.py /usr/local/bin/simple-contact/.
RUN pip3 install -r /usr/local/bin/simple-contact/requirements.txt
CMD python3 /usr/local/bin/simple-contact/simple-contact.py