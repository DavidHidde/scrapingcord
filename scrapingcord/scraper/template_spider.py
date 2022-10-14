import functools
from typing import Generator, Callable, Union, Iterable

from discord import Client
from scrapy import Spider, Request
from scrapy.http import Response

from scrapingcord.scraper.template_item import TemplateItem
from scrapingcord.utils import ScrapingImplementation, MessageTemplate


class TemplateSpider(Spider):
    """
    Spider that crawls based on the given template
    """
    name: str = 'template_spider'
    client: Client
    __mapping: dict

    def __init__(self, mapping: dict, client: Client):
        """
        :param mapping: Mapping created in the PingScraper
        """
        self.__mapping = mapping
        self.client = client

    def start_requests(self) -> Generator[Request, None, None]:
        """
        Start making requests with the specified callbacks based on the mapping
        """
        for implementation_dict in self.__mapping:
            for url in implementation_dict.get(ScrapingImplementation.KEY_URLS, []):
                yield Request(
                    url,
                    self.__parse_decorator(
                        implementation_dict.get(ScrapingImplementation.KEY_PARSER, self.parse),
                        implementation_dict.get(ScrapingImplementation.KEY_TEMPLATE)
                    )
                )

    def parse(self, response, **kwargs) -> None:
        """
        Standard empty parsing function to catch implementations with missing parsing functions

        :param response:
        :param kwargs:
        :return:
        """
        pass

    def __parse_decorator(
            self,
            parsing_func: Callable[[Response], Union[Iterable[Request], dict]],
            message_template: MessageTemplate
    ):
        """
        Decorator for combining a dict response and a message template into a TemplateItem

        :param parsing_func: Function used for parsing Scrapy responses. Should follow https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.parse but return a dict for the final result
        :param message_template: The message template that applies to this implementation
        """
        @functools.wraps(parsing_func)
        def combine_item_response(*args, **kwargs):
            response = parsing_func(*args, **kwargs)
            return TemplateItem(template=message_template, template_data=response) if type(response) == dict else response

        return combine_item_response
