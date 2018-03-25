FROM python:3.6

RUN mkdir -p /usr/local/bin/notifier/
COPY requirements.txt /usr/local/bin/notifier/.
COPY notifier.py /usr/local/bin/notifier/.
RUN pip3 install -r /usr/local/bin/notifier/requirements.txt
CMD python3 /usr/local/bin/notifier/notifier.py
