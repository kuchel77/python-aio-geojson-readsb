"""Readsb feed entry."""
from datetime import datetime
from typing import Optional, Tuple

import logging
import pytz
import geopy.distance


_LOGGER = logging.getLogger(__name__)

class ReadsbFeedEntry():
    """Flight Air Map Incidents feed entry."""

    def __init__(self, home_coordinates, aircraft_coordinates, feature):
        """Initialise this service."""
        self._home_coordinates = home_coordinates
        self._aircraft_coordinates = aircraft_coordinates
        self._feature = feature

    def _search_in_properties(self, name):
        """Find an attribute in the feed entry's properties."""

        if (
            self._feature and self._feature[name]
        ):
            return self._feature[name]
        return None

    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("flightno")

    @property
    def external_id(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("reg")

    @property
    def flight_num(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("flightno")

    @property
    def aircraft_registration(self) -> str:
        """Return the y of this entry."""
        return self._search_in_properties("reg")

    @property
    def aircraft_icao(self) -> str:
        """Return the y of this entry."""
        return self._search_in_properties("aircraft_icao")

    @property
    def aircraft_type(self) -> str:
        """Return the location of this entry."""
        return self._search_in_properties("type")

    @property
    def departure_airport(self) -> str:
        """Return the y of this entry."""
        if self._search_in_properties("route").find("-") != -1:
            route = self._search_in_properties("route").split('-')
            return route[0]
        return None

    @property
    def arrival_airport(self) -> str:
        """Return the location of this entry."""
        if self._search_in_properties("route").find("-") != -1:
            route = self._search_in_properties("route").split('-')
            return route[-1]
        return None

    @property
    def altitude(self) -> str:
        """Return the location of this entry."""
        if self._search_in_properties("altitude") is not None:
            altitude = self._search_in_properties("altitude")
        else:
            altitude = 0
        return altitude

    @property
    def selected_altitude(self) -> str:
        """Return the location of this entry."""
        if self._search_in_properties("selected_altitude") is not None:
            altitude = self._search_in_properties("selected_altitude")
        else:
            altitude = 0
        return altitude

    @property
    def squawk(self) -> str:
        """Return the location of this entry."""
        squawk = self._search_in_properties("squawk")
        return squawk

    @property
    def heading(self) -> str:
        """Return the location of this entry."""
        heading = self._search_in_properties("heading")
        if heading is not None:
            return heading
        return None

    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        last_update = self._search_in_properties("lu")
        if last_update is not None:
            publication_date = datetime.fromtimestamp(int(last_update), tz=pytz.utc)
            return publication_date
        return None

    @property
    def coordinates(self) -> Optional[Tuple[float, float]]:
        """Return the best coordinates (latitude, longitude) of this entry."""
        if self._aircraft_coordinates:
            return self._aircraft_coordinates
        return None

    @property
    def distance(self) -> float:
        """Return the distance between home coordinates and aircraft coordinates."""
        if self._home_coordinates != None and self._aircraft_coordinates != None:
            return round(geopy.distance.geodesic(self._home_coordinates, self._aircraft_coordinates).km,2)
        return None
