from typing import Union

from aiohttp import ClientSession


class DiscordHttpClient:
    """
    Client for making HTTP calls to the Discord API
    """
    DISCORD_API_BASE_URL = 'https://discord.com/api'
    API_VERSION = 'v10'

    __token: str
    __session: Union[ClientSession, None] = None

    def __init__(self, token: str):
        """
        Create a new HTTP client and set the token

        :param token: The Discord token for the bot user
        """
        self.__token = token

    def create_api_url(self, api_route: str):
        """
        Create a URL by concatenating parts to the base Discord API URL

        :param api_route: The specific API route (should not start with a '/')
        :return: Full URL to the Discord API
        """
        return '/'.join([self.DISCORD_API_BASE_URL, self.API_VERSION, api_route])

    async def create_dm(self, recipient_id: str) -> dict:
        """
        Create a DM channel with a specific User
        https://discord.com/developers/docs/resources/user#create-dm

        :param recipient_id: The Snowflake ID of the User
        :return: A DM Channel object https://discord.com/developers/docs/resources/channel#channel-object
        """
        async with self.get_session().post(
            self.create_api_url('users/@me/channels'),
            json={'recipient_id': recipient_id}
        ) as response:
            return await response.json()

    async def create_message(self, channel_id: str, message_contents: dict) -> dict:
        """
        Send a message to a specific channel
        https://discord.com/developers/docs/resources/channel#create-message

        :param channel_id: The ID of the guild or DM channel
        :param message_contents: https://discord.com/developers/docs/reference#message-formatting
        :return:
        """
        async with self.get_session().post(
            self.create_api_url(f"channels/{channel_id}/messages"),
            json=message_contents
        ) as response:
            return await response.json()


    def get_session(self) -> ClientSession:
        """
        Lazy getter for the ClientSession

        :return: A configured ClientSession
        """
        if self.__session is None:
            headers = {
                'Authorization': 'Bot ' + self.__token,
                'User-Agent': 'ScraPingCord (https://github.com/DavidHidde/scrapingcord, 0.1)'
            }
            self.__session = ClientSession(headers=headers)

        return self.__session

    async def close(self):
        """
        Close the client properly by closing the session
        """
        if self.__session is not None:
            await self.__session.close()