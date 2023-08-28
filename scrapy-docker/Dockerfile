FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .

CMD [ "python3", "crawler/spiders/wttj_links.py" ]