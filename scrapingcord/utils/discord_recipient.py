class DiscordRecipient:
    """
    Data container for a type of discord recipient, identified by an ID given in Discord
    """
    TYPE_USER = 'user'
    TYPE_CHANNEL = 'channel'

    recipient_id: str
    recipient_type: str

    def __init__(
            self,
            recipient_id: str, recipient_type: str
    ) -> None:
        """
        :param recipient_id: Unique ID of the user/channel/thread
        :param recipient_type: Either TYPE_USER or TYPE_CHANNEL
        """
        self.recipient_id = recipient_id
        self.recipient_type = recipient_type

    def is_user(self) -> bool:
        """
        :return: True if this recipient is a user, else False
        """
        return self.recipient_type == self.TYPE_USER

    def is_channel(self) -> bool:
        """
        :return: True if this recipient is a channel, else False
        """
        return self.recipient_type == self.TYPE_CHANNEL
