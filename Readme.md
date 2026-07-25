# WEATHER APP
## Backend Development
The FastAPI backend currently includes:
- Root API endpoint
- Health-check endpoint
- CORS configuration for the React development server
- Automatic Swagger documentation
- Initial automated endpoint tests

### Run the Backend
```bash
cd backend
.\tech\Scripts\Activate.ps1
uvicorn app.main:app --reload

## MongoDB Configuration

The application uses MongoDB Atlas for weather-record persistence.

Create `backend/.env` using `backend/.env.example`:

```env
MONGODB_URI=<your MongoDB Atlas connection string>
MONGODB_DATABASE=WeatherApp
MONGODB_COLLECTION=Weather_records

## MongoDB Application Integration

FastAPI creates one asynchronous MongoDB client during application startup and closes it during application shutdown.

The MongoDB resources are made available to API endpoints through FastAPI application state.

The health endpoint verifies both the API and database connection:
```text
GET /api/health

## Request Validation

WeatherApp API uses Pydantic models to validate API requests.

Create requests support either:
- A city, town, or postal-code location
- A complete latitude and longitude pair

Validation rules include:
- Location must contain at least two characters
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- End date cannot be earlier than start date
- Date range cannot exceed five days
- Temperature unit must be Celsius or Fahrenheit
- Unexpected fields are rejected

Separate models are used for create requests, update requests,location results, weather data, forecast data, air quality, and API responses.