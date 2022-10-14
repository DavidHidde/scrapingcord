from discord import Client
from scrapy.exceptions import DropItem

from scrapingcord.scraper.template_item import TemplateItem
from scrapingcord.scraper.template_spider import TemplateSpider
from scrapingcord.utils import DiscordRecipient


class PingPipeline:
    """
    Pipeline that pings using Discord based on the given template
    """
    __client: Client
    __recipient_cache: dict

    def open_spider(self, spider: TemplateSpider):
        """
        Set the Discord client beforehand
        :param spider: The running spider
        """
        self.__client = spider.client
        if self.__client is None:
            raise Exception('Missing Discord client')

    async def process_item(self, item: TemplateItem, spider: TemplateSpider):
        template = item.get('template')
        template_data = item.get('template_data')
        # Check for missing data
        if template is None or template_data is None:
            raise DropItem(f"Missing data: template={template is None}, template_data={template_data is None}")

        for message, recipient in template.get_message_list(template_data):
            await self.get_recipient(recipient).send(content=message)

    def get_recipient(self, recipient: DiscordRecipient):
        """
        Get a user/channel and cache it locally
        :param recipient:
        :return: The fetched recipient
        """
        key = recipient.get_unique_key()
        fetched = self.__recipient_cache.get(key)
        if fetched is None:
            if recipient.recipient_type == DiscordRecipient.TYPE_USER:
                fetched = self.__client.get_user(recipient.recipient_id)
            elif recipient.recipient_type == DiscordRecipient.TYPE_CHANNEL:
                fetched = self.__client.get_channel(recipient.recipient_id)
            else:
                raise DropItem('Unable to get user/channel')
            self.__recipient_cache[key] = fetched

        return fetched
