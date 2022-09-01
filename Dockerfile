# Build step #1: Installing and moving the app
FROM python:3.10

WORKDIR /usr/src/scrapingcord

COPY scrapingcord/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./scrapingcord .

# Build step #2: Run the scraper
CMD ["scrapy", "crawl", "message_spider"]