from typing import Generator

from scrapy import Spider, Request
from scrapy.http import Response

from scrapingcord.discord import MessageSender
from scrapingcord.utils import ScrapingImplementation


class TemplateSpider(Spider):
    """
    Spider that crawls based on the given template.
    This spider has none of the important logic, since it is located in the pipeline and middleware
    """
    name: str = 'template_spider'
    message_sender: MessageSender
    __mapping: dict

    def __init__(self, mapping: dict, message_sender: MessageSender):
        """
        :param mapping: Mapping created in the PingScraper
        :param message_sender: The message sender that should be used to send messages
        """
        self.__mapping = mapping
        self.message_sender = message_sender

    def start_requests(self) -> Generator[Request, None, None]:
        """
        Start making requests with the specified callbacks based on the mapping
        """
        for implementation_dict in self.__mapping.values():
            for url in implementation_dict.get(ScrapingImplementation.KEY_URLS, []):
                yield Request(
                    url,
                    implementation_dict.get(ScrapingImplementation.KEY_PARSER, self.parse),
                    meta=implementation_dict
                )

    def parse(self, response: Response, **kwargs) -> None:
        """
        Standard empty parsing function to catch implementations with missing parsing functions

        :param response:
        :param kwargs:
        :return:
        """
        pass
