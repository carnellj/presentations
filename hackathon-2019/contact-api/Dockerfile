FROM python:3.6

RUN mkdir -p /usr/local/bin/contact/
COPY requirements.txt /usr/local/bin/contact/.
COPY contact.py /usr/local/bin/contact/.
COPY DB.py /usr/local/bin/contact/.
COPY log.py /usr/local/bin/contact/.
COPY utils.py /usr/local/bin/contact/.
RUN pip3 install -r /usr/local/bin/contact/requirements.txt
CMD python3 /usr/local/bin/contact/contact.py