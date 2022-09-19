"""Readsb feed."""
from array import ArrayType
import logging
from typing import Optional

from typing import Tuple, List
import json
import asyncio
import aiohttp
from aiohttp import ClientSession


from .feed_entry import ReadsbFeedEntry
from .consts import (
    DEFAULT_REQUEST_TIMEOUT,
    T_FEED_ENTRY,
    UPDATE_ERROR,
    UPDATE_OK,
    UPDATE_OK_NO_DATA,
)

_LOGGER = logging.getLogger(__name__)


class ReadsbFeed():
    """Flight Air Map feed."""

    def __init__(self,
                 websession: ClientSession,
                 coordinates,
                 url,
                 filter_radius=None):
        self._websession = websession
        self._coordinates = coordinates
        self._url = url
        self._filter_radius=filter_radius
        self._home_coordinates = None
        self._last_timestamp = None

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius)

    def _new_entry(self, home_coordinates, aircraft_coordinates, feature):
        """Generate a new entry."""
        return ReadsbFeedEntry(home_coordinates, aircraft_coordinates, feature)

    def _client_session_timeout(self) -> int:
        """Define client session timeout in seconds. Override if necessary."""
        return DEFAULT_REQUEST_TIMEOUT

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        return None

    def _extract_last_timestamp(self, feed_entries):
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(filter(
                None, [entry.publication_date for entry in feed_entries]),
                           reverse=True)
            if len(dates) > 0:
                return dates[0]
        return None

    async def _fetch(
        self, method: str = "GET", headers=None, params=None
    ) -> Tuple[str, Optional[ArrayType]]:
        """Fetch GeoJSON data from external source."""
        try:
            timeout = aiohttp.ClientTimeout(total=self._client_session_timeout())
            async with self._websession.request(
                method, self._url, headers=headers, params=params, timeout=timeout
            ) as response:
                try:
                    response.raise_for_status()
                    text = await response.text()
                    feature_collection = json.loads(text)
                    return UPDATE_OK, feature_collection
                except aiohttp.client_exceptions.ClientError as client_error:
                    _LOGGER.warning(
                        "Fetching data from %s failed with %s", self._url, client_error
                    )
                    return UPDATE_ERROR, None
                except json.JSONDecodeError as decode_ex:
                    _LOGGER.warning(
                        "Unable to parse JSON from %s: %s", self._url, decode_ex
                    )
                    return UPDATE_ERROR, None
        except aiohttp.client_exceptions.ClientError as client_error:
            _LOGGER.warning(
                "Requesting data from %s failed with " "client error: %s",
                self._url,
                client_error,
            )
            return UPDATE_ERROR, None
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Requesting data from %s failed with " "timeout error", self._url
            )
            return UPDATE_ERROR, None

    async def _update_internal(
        self
    ) -> Tuple[str, Optional[List[T_FEED_ENTRY]]]:
        """Update from external source and return filtered entries."""
        status, data = await self._fetch()
        if status == UPDATE_OK:
            if data:
                entries = []
                home_coordinates = [data['user']['user_lat'],data['user']['user_lon']]
                # Extract data from feed entries.
                for plane in data["aircraft"]:
                    if "lat" in data["aircraft"][plane] and "lon" in data["aircraft"][plane]:
                        aircraft_coordinates = [data["aircraft"][plane]["lat"],data["aircraft"][plane]["lon"]]
                        entries.append(
                            self._new_entry(home_coordinates, aircraft_coordinates, data["aircraft"][plane])
                        )

                #filtered_entries = filter_function(entries)
                self._last_timestamp = None #self._extract_last_timestamp(entries)
                return UPDATE_OK, entries
            return UPDATE_OK, None
        elif status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        else:
            # Error happened while fetching the feed.
            self._last_timestamp = None
            return UPDATE_ERROR, None

    async def update(self) -> Tuple[str, Optional[List[T_FEED_ENTRY]]]:
        """Update from external source and return filtered entries."""
        return await self._update_internal()
