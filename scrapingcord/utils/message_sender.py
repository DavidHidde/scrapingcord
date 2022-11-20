from abc import ABC, abstractmethod

from scrapingcord.utils import MessageTemplate


class MessageSender(ABC):
    """
    Interface describing a service that can send messages
    """

    @abstractmethod
    async def add_message(self, template: MessageTemplate, template_data: dict) -> bool:
        """
        Add a message to send

        :param template: The message template to send
        :param template_data: The data to substitute in the template
        :return True if adding the message went well, else False
        """
        pass

    @abstractmethod
    async def flush(self) -> None:
        """
        Send all lingering messages and close all connections
        """
        pass
