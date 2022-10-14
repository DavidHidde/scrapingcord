class DiscordRecipient:
    """
    Data container for a type of discord recipient, identified by an ID given in Discord
    """
    TYPE_USER = 'user'
    TYPE_CHANNEL = 'channel'

    recipient_id: int
    recipient_type: str

    def __init__(
            self,
            recipient_id: int, recipient_type: str
    ) -> None:
        """
        :param recipient_id: Unique ID of the user/channel/thread
        :param recipient_type: Either TYPE_USER or TYPE_CHANNEL
        """
        self.recipient_id = recipient_id
        self.recipient_type = recipient_type

    def get_unique_key(self) -> str:
        """
        :return: A unique key based on the type and id of the recipient
        """
        return f"{self.recipient_type}_{self.recipient_id}"
