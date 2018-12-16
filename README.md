# godmusic
Enernal sunshine of a divine music catalog database

## requirements

### python
scrapy
selenium
pymongo (optional for persisting catalog with mongodb)

### database

mongodb (optional for persisting catalog)

## run scrapy spider
scrapy runspider spider/SPIDER_SCRIPT

## scrapped radios

#LifeRadio Italy (main)

- url:    https://lifegate.it/radio-sound
- spider: spiders/lifegate_spider.py

## Warning
When you run the code in your local env, make sure to edit `MONGO_URI` and `MONGO_DATABASE` in `scrapy_spider/settings.py`.
