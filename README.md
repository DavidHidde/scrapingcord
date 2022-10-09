# ScraPingCord
A simple implementation of a Scrapy webscraper + a simple Discord ping bot in Python 3.10.

This framework serves a very simple purpose: scrape content off the internet, use this to generate messages and publish these messages to recipients using Discord. This includes the following features:
* Easy implementation: only elements that actually differ between implementations have to be written
* Use of the popular frameworks [discord.py](https://github.com/Rapptz/discord.py) and [Scrapy](https://scrapy.org/)
* Easy integration into existing Scrapy or Discord.py setups by being able to pass settings/instances

The main application of this is to generate Discord notifications based on web content, like custom webhooks.

Implementation requirements are encapsulated by the `ScrapingImplentation` class:
* A message template (with recipients) (see `MessageTemplate`)
* A parser function that follows [Scrapy standards](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.parse)
* A set of starting urls

## Limitations
Currently, dynamic message templates based on scraped content are not supported.
