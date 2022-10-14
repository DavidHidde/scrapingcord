import scrapy

from scrapingcord.utils import MessageTemplate


class TemplateItem(scrapy.Item):
    """
    Simple custom item containing a message template and the data to fill it
    """
    template: MessageTemplate
    template_data: dict
