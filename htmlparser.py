"""Parses channel IDs from xmlurl attributes in tags."""
from html.parser import HTMLParser

class htxmlParser(HTMLParser):
    def __init__(self):
        """Holds the final url(s) for usage, initializes empty state"""
        HTMLParser.__init__(self) # random errors attributed to being called 'htxmlParser' are fixed by initializing with parent class
        self.subscription_urls = []
        self.reset()

    def _format_channelid(self, link):
        """Returns the id of a channel url"""
        return link[52:]

    def handle_starttag(self, tag, attrs=None):
        """"Appends xmlurl values from an xml list of subscriptions to subscription_urls."""
        for datum in attrs:
            if datum[0] == 'xmlurl':
                self.subscription_urls.append( "https://www.youtube.com/channel/" + self._format_channelid(datum[1]) + "?sub_confirmation=1" )
