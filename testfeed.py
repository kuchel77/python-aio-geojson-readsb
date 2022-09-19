""" This is a test of the readsb feed """
import asyncio
from aiohttp import ClientSession
from aio_readsb import ReadsbFeed
async def main() -> None:
    """ Main function """
    async with ClientSession() as websession:
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 50 km
        feed = ReadsbFeed(websession,
                                (-33.0, 150.0),
                                "http://192.168.0.245:30053/ajax/aircraft?_=1663478109932",
                                filter_radius=20000)

        status, entries = await feed.update()
        print(status)
        print(entries)
        for entry in entries:
            print(entry.coordinates)
            print(entry.flight_num)
            print(entry.departure_airport)
            print(entry.arrival_airport)
            print(entry.squawk)
            print(entry.altitude)
            print(entry.aircraft_type)
            print(entry.flight_num)
            print(entry.aircraft_registration)
            print(entry.distance)

asyncio.get_event_loop().run_until_complete(main())
