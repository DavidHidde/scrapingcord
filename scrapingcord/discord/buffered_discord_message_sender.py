from scrapingcord.discord.discord_message_sender import DiscordMessageSender
from scrapingcord.utils import MessageTemplate


class BufferedDiscordMessageSender(DiscordMessageSender):
    """
    A Discord message sender which sends all messages in a single message when it closes.
    Note that Discord has a content limit and no message will be sent if it errors out.
    """
    __messages_buffer: dict = {}

    async def add_message(self, template: MessageTemplate, template_data: dict) -> bool:
        """
        Add the message to the buffer per recipient

        :param template: The message template to send
        :param template_data: The data to substitute in the template
        :return Always True since we don't send the messages yet
        """
        for message, recipient in template.get_message_list(template_data):
            recipient_buffer = self.__messages_buffer.get(recipient.recipient_id, {
                'recipient': recipient,
                'messages': []
            })
            recipient_buffer['messages'].append(message)
            self.__messages_buffer[recipient.recipient_id] = recipient_buffer

        return True

    async def flush(self) -> None:
        """
        Send all messages and close the client
        """
        for recipient_dict in self.__messages_buffer.values():
            await self.send_message(
                recipient_dict['recipient'],
                {'content': '\n'.join(recipient_dict['messages'])}
            )

        await super().flush()
