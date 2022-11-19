import functools
import logging
from asyncio import sleep, Lock
from typing import Union

from aiohttp import ClientSession


def rate_limit(api_call_func):
    """
    Decorator for rate-limiting Discord API calls
    """

    @functools.wraps(api_call_func)
    async def retry_on_rate_limit(*args, **kwargs):
        async with DiscordHttpClient.lock:
            response = await api_call_func(*args, **kwargs)
            if response.get('retry_after') is not None:
                await sleep(float(response.get('retry_after')))
                response = await api_call_func(*args, **kwargs)

            return response

    return retry_on_rate_limit


def log_api_errors(api_call_func):
    """
    Log errors if they are present in the API response
    """

    @functools.wraps(api_call_func)
    async def log_errors_in_response(*args, **kwargs):
        response = await api_call_func(*args, **kwargs)
        if response.get('errors'):
            logging.getLogger('DiscordHttpClient').warning('Encountered error in API response: ' + str(response))
        return response

    return log_errors_in_response


class DiscordHttpClient:
    """
    Client for making HTTP calls to the Discord API
    """
    DISCORD_API_BASE_URL = 'https://discord.com/api'
    API_VERSION = 'v10'

    __token: str
    __session: Union[ClientSession, None] = None

    # Lock to avoid problems when we are being rate limited
    lock = Lock()

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

    @log_api_errors
    @rate_limit
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

    @log_api_errors
    @rate_limit
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
                'User-Agent': 'ScraPingCord (https://github.com/DavidHidde/scrapingcord, 1.0)'
            }
            self.__session = ClientSession(headers=headers)

        return self.__session

    async def close(self):
        """
        Close the client properly by closing the session
        """
        if self.__session is not None:
            await self.__session.close()
