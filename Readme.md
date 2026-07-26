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

## Location Search
The application validates location input through the Open-Meteo Geocoding API.

Supported inputs include:
- City
- Town
- Region
- Country
- ZIP or postal code

### Endpoint
```text
GET /api/locations/search?q=Binghamton&limit=5

## Weather Forecast Integration

WeatherWise retrieves real weather data through the Open-Meteo
Forecast API.

### Endpoint

```text
GET /api/weather

## Create Weather Record

WeatherApp can resolve a location, retrieve live weather data, and save the complete result in MongoDB.

### Endpoint
```text
POST /api/weather-records

## Read Weather Records

WeatherApp allows users to retrieve previously stored weather requests from MongoDB.

### Read All Records

```text
GET /api/weather-records

## Update Weather Records

Users can update selected fields on an existing weather record.

### Endpoint

```text
PATCH /api/weather-records/{record_id}

## Delete Weather Records

Users can permanently remove a stored weather record from MongoDB collections.

### Endpoint

```text
DELETE /api/weather-records/{record_id}

## Data Export

WeatherApp supports exporting MongoDB weather records stored in JSON and CSV formats.

### JSON Export

```text
GET /api/weather-records/export/json

## Frontend Structure

The WeatherApp frontend is built with React and Vite.

### Pages
It comprises of following pages
- Dashboard
- Saved Weather Records
- About
- Not Found

### Dashboard Layout

The dashboard currently includes:
- Location and date-range form
- Temperature-unit selector
- Current-location button
- Current-weather placeholder
- Travel-insight placeholder
- Five-day forecast placeholder

The frontend uses React Router for client-side navigation.

### Responsive Design

The application follows a desktop-first responsive approach using:
- CSS Grid
- Flexbox
- Flexible container widths
- Responsive font sizing
- Tablet and mobile media queries
- Stacked form and card layouts

### Run the Frontend

```bash
cd frontend
npm install
npm run dev

## Frontend API Integration

The React frontend communicates with FastAPI through Axios.

### Frontend Environment

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000

## Current Location

WeatherApp supports retrieving weather from the user's current browser location.

### Workflow
1. User clicks **Use Current Location**
2. The browser requests location permission
3. Latitude and longitude are returned to React
4. React sends the coordinates to `GET /api/weather`
5. FastAPI retrieves the weather information
6. The dashboard displays the current conditions

### Permission Handling

The application handles:
- Location permission denied
- Position unavailable
- Location timeout
- Unsupported browser
- FastAPI connection failure

Browser geolocation requires user permission. The deployed frontend must use HTTPS. Local development can use `localhost`.

## Five-Day Forecast

WeatherApp displays real daily forecast information returned by FastAPI.

Each forecast card includes:
- Day and date
- Weather condition
- Weather icon
- Maximum temperature
- Minimum temperature
- Precipitation probability
- Precipitation amount
- Maximum wind speed
- Sunrise
- Sunset

The forecast automatically uses the units returned by the backend:
- Fahrenheit, mph, and inches
- Celsius, km/h, and millimeters

The dashboard supports date ranges from one to five days. The number of displayed cards matches the selected range and the forecast data returned by the weather API.