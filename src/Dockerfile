FROM python:3.8
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mitmproxy
COPY config.json /
COPY main.py /
CMD /usr/local/bin/mitmdump -s /main.py