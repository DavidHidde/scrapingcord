from typing import Union, Generator

from scrapy import Request
from scrapy.http import Response

from scrapingcord.scraper import TemplateSpider, TemplateItem
from scrapingcord.utils import ScrapingImplementation


class ImplementationMapperMiddleware:
    """
    Middleware that binds the implementation to the parse response
    """
    def process_spider_output(
            self,
            response: Response,
            result: Generator[Union[Request, dict], Union[Request, dict], None],
            spider: TemplateSpider
    ) -> Generator[Union[Request, dict], Union[Request, dict], None]:
        """
        Couple the implementation to all new requests or parse dicts into TemplateItems

        :param response: The original response for the parse function
        :param result: Generator of Requests and dicts
        :param spider:
        :return:
        """
        implementation = response.meta

        for item in result:
            if type(item) == Request:
                yield item.replace(
                    callback=(item.callback if item.callback else implementation.get(ScrapingImplementation.KEY_PARSER)),
                    meta=implementation
                )
            if type(item) == dict:
                yield TemplateItem(
                    template=implementation.get(ScrapingImplementation.KEY_TEMPLATE),
                    template_data=item
                )
