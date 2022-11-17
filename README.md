# ScraPingCord
A simple implementation of a Scrapy webscraper + a simple Discord ping bot in Python 3.10.

This framework serves a very simple purpose: scrape content off the internet, use this to generate messages and publish these messages to recipients using Discord. This includes the following features:
* Little prior experience needed: Only knowledge about how to scrape needed, nothing else
* Only elements that actually differ between implementations have to be written.
* Use of the flexible scraping framework [Scrapy](https://scrapy.org/), allowing for integration with other Scrapy setups. The application is mainly a scraper by design, with message sending second.

The main application of this is to generate Discord notifications based on web content, like custom webhooks.

## Build your own implementation
Implementation requirements are encapsulated by the `ScrapingImplentation` class:
* A message template (with recipients) (see `MessageTemplate`)
* A parser function that generates either [Scrapy Requests](https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request) and/or a dictionaries with template values.
* A set of starting urls

An example of a very simple scraper implementation for scraping country names:
```python
DISCORD_TOKEN = '<YOUR DISCORD BOT TOKEN>'
START_URLS = ['https://www.scrapethissite.com/pages/simple/']

def parse(response: Response) -> Generator[Union[Request, dict], Union[Request, dict], None]:
    for idx, country_selector in enumerate(response.xpath("//h3[contains(@class, 'country-name')]")):
        yield {'country': country_selector.xpath('text()')[1].get().strip()}

        # For this example, just take the first 10 countries
        if idx >= 10:
            break

implementation = ScrapingImplementation(
    'country_scraper_example',
    START_URLS,
    parse,
    MessageTemplate('I found this country: {country}', [DiscordRecipient('<YOUR DISCORD USER ID>', DiscordRecipient.TYPE_USER)])
)

service = PingScraper()
service.register_implementation(implementation)
service.run(BufferedDiscordMessageSender(DISCORD_TOKEN))
```
This implementation uses the `BufferedDiscordMessageSender`, which concatenates all messages for a recipient into a single message. The `DirectDiscordMessageSender` can also be used to send all messages individually, but this sender should be avoided due to rate-limiting. Custom senders can be made using the `DiscordMessageSender`.
