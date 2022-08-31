# ScraPingCord
A simple combination framework of a Scrapy webscraper + a simple Discord ping bot in Python 3.10.

This framework serves a very simple purpose: scrape content off the internet, use this to generate messages and publish these messages to recipients using Discord. This includes the following features:
* Containerized operation to allow for high up-time
* Abstract framework to allow custom spiders, message templating and message recipients
* Use of the popular frameworks [discord.py](https://github.com/Rapptz/discord.py) and [Scrapy](https://scrapy.org/)

The main application of this is to generate multi-platform notifications for free.

Requirements:
* Docker with compose
* A Discord bot setup with a token and the correct permissions for your needs
* Implementations of the `MessageSpider` and the `MessagePipeline` to implement the scraping and message templating respectively.
