from typing import Optional, Callable, Iterable, Union

from discord import Client
from scrapy import Item, Request
from scrapy.http import Response

from scrapingcord.utils import ScrapingImplementation, MessageTemplate


class PingScraper:
    """
    Main class that handles setting up the scraper and manages implementations
    """
    __mapping: dict = {}

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

    def register_parser(self, key: str, parser_func: Callable[[Response], Union[Iterable[Request], Item]]):
        """
        Add/replace parser function of an implementation

        :param key: The id of the implementation
        :param parser_func: Function used for parsing Scrapy responses. Should follow https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.parse
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
        settings: Optional[dict] = None,
        token: Optional[str] = None,
        client: Optional[Client] = None
    ) -> None:
        """
        Runs the scraper with the registered implementations.
        If no discord client is given or can be initiated, an error will be thrown.

        :param settings: Scrapy settings dictionary. Uses default settings if not given
        :param token: The Discord bot token. Nullable if the client is set
        :param client: The Discord bot client. Nullable if the token is set
        """
        pass
