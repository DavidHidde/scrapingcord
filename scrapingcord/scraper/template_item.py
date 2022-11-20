import scrapy


class TemplateItem(scrapy.Item):
    """
    Simple custom item containing a message template and the data to fill it
    """
    template = scrapy.Field()        # MessageTemplate
    template_data = scrapy.Field()   # dict of formatting arguments
