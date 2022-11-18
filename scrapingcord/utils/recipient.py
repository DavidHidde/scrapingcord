class Recipient:
    """
    Data container for a type of recipient, identified by an ID
    """
    recipient_id: str
    recipient_type: str

    def __init__(
            self,
            recipient_id: str,
            recipient_type: str
    ) -> None:
        """
        :param recipient_id: Unique ID of the recipient
        :param recipient_type: The type of the user
        """
        self.recipient_id = recipient_id
        self.recipient_type = recipient_type
