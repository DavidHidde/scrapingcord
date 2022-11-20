from typing import Callable, Union, Iterable

from scrapy import Request
from scrapy.http import Response

from scrapingcord.utils.message_template import MessageTemplate


class ScrapingImplementation:
    """
    Container for a complete scraper implementation
    """
    KEY_URLS = 'urls'
    KEY_PARSER = 'parser'
    KEY_TEMPLATE = 'template'

    implementation_id: str
    start_urls: list[str]
    parsing_func: Callable[[Response], Union[Iterable[Request], dict]]
    message_template: MessageTemplate

    def __init__(
            self,
            implementation_id: str,
            start_urls: list[str],
            parsing_func: Callable[[Response], Union[Iterable[Request], dict]],
            message_template: MessageTemplate
    ):
        """
        :param implementation_id: The unique id for this implementation
        :param start_urls: List of starting urls for this implementation
        :param parsing_func: Function used for parsing Scrapy responses. Should follow https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.parse but return a dict for the final result
        :param message_template: The message template that this implementation should return
        """
        self.implementation_id = implementation_id
        self.start_urls = start_urls
        self.parsing_func = parsing_func
        self.message_template = message_template

    def export(self) -> dict:
        """
        :return: A PingScraper compatible dictionary
        """
        return {
            self.KEY_URLS: self.start_urls,
            self.KEY_PARSER: self.parsing_func,
            self.KEY_TEMPLATE: self.message_template
        }
