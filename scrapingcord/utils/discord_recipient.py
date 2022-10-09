from typing import Union

from discord import Thread, User
from discord.abc import GuildChannel, PrivateChannel


class DiscordRecipient:
    """
    Data container for a type of discord recipient, identified by an ID given in Discord
    """
    recipient_id: int
    recipient_type: Union[type[User], type[GuildChannel], type[Thread], type[PrivateChannel]]

    def __init__(
            self,
            recipient_id: int, recipient_type: Union[type[User], type[GuildChannel], type[Thread], type[PrivateChannel]]
    ) -> None:
        """
        :param recipient_id: Unique ID of the user/channel/thread
        :param recipient_type: The class of the recipients
        """
        self.recipient_id = recipient_id
        self.recipient_type = recipient_type

    def get_unique_key(self) -> str:
        """
        :return: A unique key based on the type and id of the recipient
        """
        return f"{self.recipient_type}_{self.recipient_id}"
