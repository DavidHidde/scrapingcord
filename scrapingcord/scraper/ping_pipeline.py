
from typing import Optional
from scrapy.exceptions import DropItem

from scrapingcord.utils import MessageSender
from scrapingcord.scraper.template_item import TemplateItem
from scrapingcord.scraper.template_spider import TemplateSpider


class PingPipeline:
    """
    Pipeline that sends a message using the MessageSender
    """
    __message_sender: Optional[MessageSender]

    def open_spider(self, spider: TemplateSpider) -> None:
        """
        Start the Discord client given the token

        :param spider: The running spider
        """
        self.__message_sender = spider.message_sender
        if self.__message_sender is None:
            raise Exception('Missing MessageSender')

    async def process_item(self, item: TemplateItem, spider: TemplateSpider) -> None:
        """
        Send the scraped messages

        :param item:
        :param spider:
        """
        template = item.get('template')
        template_data = item.get('template_data')

        # Check for missing data
        if template is None or template_data is None:
            raise DropItem(f"Missing data: template={template is None}, template_data={template_data is None}")

        # Data has been verified; get the loop and send the messages
        if not (await self.__message_sender.add_message(template, template_data)):
            raise DropItem(f"Failed sending message")
