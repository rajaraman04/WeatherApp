class LocationNotFoundError(Exception):
    def __init__(self, query):
        self.query=query
        super().__init__(f"No location found for the query: {query}")

class ExternalAPIError(Exception):
    pass