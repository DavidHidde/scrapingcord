from abc import ABC
from typing import Optional

from scrapingcord.discord import DiscordHttpClient
from scrapingcord.discord.message_sender import MessageSender
from scrapingcord.utils import DiscordRecipient


class DiscordMessageSender(MessageSender, ABC):
    """
    Abstract base class with functions for sending Discord messages.
    Keep in mind the Discord Rate limiting, so only 50 requests per second are possible
    """
    __client: DiscordHttpClient
    __user_dm_channel_cache: dict = {}

    def __init__(self, token: str):
        """
        :param token: The Discord bot token
        """
        self.__client = DiscordHttpClient(token)

    async def flush(self) -> None:
        """
        Close the client
        """
        await self.__client.close()

    async def send_message(self, recipient: DiscordRecipient, message_contents: dict) -> bool:
        """
        Send the message to the recipient. Make a DM channel first if the recipient is a user.

        :param recipient: The recipient of the message
        :param message_contents: The content dictionary of the message
        :return: True if sending the message went well, if there were errors return False
        """
        channel_id = recipient.recipient_id
        if recipient.is_user():
            channel_id = await self.get_user_dm_channel(recipient.recipient_id)

        return channel_id is not None and (await self.__client.create_message(channel_id, message_contents)).get('id') is not None

    async def get_user_dm_channel(self, recipient_id: str) -> Optional[str]:
        """
        Get the cached DM channel associated with a user.

        :param recipient_id: The user id
        :return: The channel ID if making a DM channel was successful, else None
        """
        if self.__user_dm_channel_cache.get(recipient_id) is None:
            response = await self.__client.create_dm(recipient_id)
            self.__user_dm_channel_cache[recipient_id] = response.get('id')

        return self.__user_dm_channel_cache[recipient_id]
