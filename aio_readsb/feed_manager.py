"""Feed Manager for Readsb feed."""
from aiohttp import ClientSession

from .feed import ReadsbFeed

class ReadsbFeedManager():
    """Feed Manager for Readsb feed."""

    def __init__(self,
                 websession: ClientSession,
                 generate_callback,
                 update_callback,
                 remove_callback,
                 coordinates=None,
                 feed_url=None,
                 filter_radius=None):
        """Initialize the Readsb Manager."""
        feed = ReadsbFeed(
            websession,
            coordinates,
            feed_url,
            filter_radius)
