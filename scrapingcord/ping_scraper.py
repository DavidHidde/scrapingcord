import asyncio
from typing import Optional, Callable, Iterable, Union

from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response

from scrapingcord.scraper import TemplateSpider
from scrapingcord.utils import ScrapingImplementation, MessageTemplate, MessageSender


class PingScraper:
    """
    Main class that handles setting up the scraper and manages implementations
    """
    __mapping: dict = {}

    SCRAPER_SETTINGS = {
        'BOT_NAME': 'scrapingcord',
        'USER_AGENT': 'scrapingcord',
        'ROBOTSTXT_OBEY': True,
        'LOG_LEVEL': 'WARNING',
        'ITEM_PIPELINES': {
            'scrapingcord.scraper.PingPipeline': 300,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapingcord.scraper.ImplementationMapperMiddleware': 543,
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    def register_implementation(self, implementation: ScrapingImplementation):
        """
        Add an implementation to the scraper

        :param implementation: The implementation to be added
        :return: This instance
        """
        self.__mapping[implementation.implementation_id] = implementation.export()
        return self

    def register_start_urls(self, key: str, urls: list[str]):
        """
        Add/replace start urls of an implementation

        :param key: The id of the implementation
        :param urls: List of start urls
        :return: This instance
        """
        if self.__mapping.get(key) is None:
            self.__mapping[key] = {}

        self.__mapping[key][ScrapingImplementation.KEY_URLS] = urls
        return self

    def register_parser(self, key: str, parser_func: Callable[[Response], Union[Iterable[Request], dict]]):
        """
        Add/replace parser function of an implementation

        :param key: The id of the implementation
        :param parser_func: Function used for parsing Scrapy responses. Should follow https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.parse but return a dict for the final result
        :return: This instance
        """
        if self.__mapping.get(key) is None:
            self.__mapping[key] = {}

        self.__mapping[key][ScrapingImplementation.KEY_PARSER] = parser_func
        return self

    def register_message_template(self, key: str, message_template: MessageTemplate):
        """
        Add/replace the message template of an implementation

        :param key: The id of the implementation
        :param message_template: The message template for the implementation
        :return: This instance
        """
        if self.__mapping.get(key) is None:
            self.__mapping[key] = {}

        self.__mapping[key][ScrapingImplementation.KEY_TEMPLATE] = message_template
        return self

    def run(
            self,
            message_sender: MessageSender,
            settings: Optional[dict] = None
    ) -> None:
        """
        Runs the scraper with the registered implementations.
        Can't be run inside a asyncio loop and also ends with a asyncio loop.

        :param message_sender: The message sender that should be used to send messages
        :param settings: Scrapy settings dictionary. Uses default settings if not given
        """
        settings = settings if settings is not None else self.SCRAPER_SETTINGS

        process = CrawlerProcess(settings=settings)
        process.crawl(TemplateSpider, mapping=self.__mapping, message_sender=message_sender)
        process.start()
        asyncio.run(message_sender.flush())
