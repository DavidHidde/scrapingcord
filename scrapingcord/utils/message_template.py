from typing import Union

from scrapingcord.utils.discord_recipient import DiscordRecipient


class MessageTemplate:
    """
    A message template consisting of a formattable string and the recipients
    """
    __formattable_message: str
    __recipients: list[DiscordRecipient]

    def __init__(self, message_template: str, recipients: list[DiscordRecipient]) -> None:
        """
        :param message_template: A formattable string, e.g.:
            'My template message for my favourite users {name} and {second_name}' -> {name: Monthy, second_name: Python}
            'My template message for my favourite users {0} and {1}' -> [Monthy, Python]
            'My template message for my favourite users {} and {}' -> [Monthy, Python]
        :param recipients: A list of all recipients the message should be sent to
        """
        self.__formattable_message = message_template
        self.__recipients = recipients

    def get_message_list(self, message_args: Union[list, dict]) -> list[tuple[str, DiscordRecipient]]:
        """
        Returns a list of the messages that should be sent to which recipient

        :param message_args: The arguments that can be used for formatting the string
        :return: A list of tuples containing the message and recipient
        """
        message = self.__formattable_message.format(**message_args) if \
            type(message_args) == dict else self.__formattable_message.format(*message_args)
        return [(message, recipient) for recipient in self.__recipients]
