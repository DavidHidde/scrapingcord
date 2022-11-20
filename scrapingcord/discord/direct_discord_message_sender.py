from scrapingcord.discord.discord_message_sender import DiscordMessageSender
from scrapingcord.utils import MessageTemplate


class DirectDiscordMessageSender(DiscordMessageSender):
    """
    A Discord message sender which immediately send any message added
    """

    async def add_message(self, template: MessageTemplate, template_data: dict) -> bool:
        """
        Send the message to the recipient directly. Make a DM channel first if the recipient is a user.

        :param template: The message template to send
        :param template_data: The data to substitute in the template
        :return True if adding the message went well, else False
        """
        for message, recipient in template.get_message_list(template_data):
            if not (await self.send_message(recipient, {'content': message})):
                return False

        return True
