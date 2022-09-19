"""Flight Air Map constants."""
from typing import TypeVar
from .feed_entry import ReadsbFeedEntry
ATTRIBUTION = "readsb Data"

CUSTOM_ATTRIBUTE = 'custom_attribute'

DEFAULT_REQUEST_TIMEOUT = 10

UPDATE_OK = "OK"
UPDATE_OK_NO_DATA = "OK_NO_DATA"
UPDATE_ERROR = "ERROR"

T_FEED_ENTRY = TypeVar("T_FEED_ENTRY", bound=ReadsbFeedEntry)
