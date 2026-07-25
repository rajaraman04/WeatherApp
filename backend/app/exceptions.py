class LocationNotFoundError(Exception):
    def __init__(self, query):
        self.query=query
        super().__init__(f"No location found for the query: {query}")

class ExternalAPIError(Exception):
    pass

class InvalidWeatherRecordIdError(Exception):
    def __init__(self, record_id):
        self.record_id = record_id
        super().__init__(f"Invalid weather record ID: {record_id}")

class WeatherRecordNotFoundError(Exception):
    def __init__(self, record_id: str) -> None:
        self.record_id = record_id
        super().__init__(f"Weather record not found: {record_id}")