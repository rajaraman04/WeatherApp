# WeatherApp

WeatherApp is a full-stack weather and travel-planning application.

Users can search for a location, use their current browser location, view current weather conditions, compare a forecast for up to five days, check air quality, and receive simple travel recommendations.

Users can also save weather searches to MongoDB, update saved records, delete records, and export the stored data as JSON or CSV.

The project was built using React, FastAPI, MongoDB Atlas, and Open-Meteo APIs.

---

## Live Demo

- Frontend: [https://weather-app-mu-ten-48.vercel.app/](https://weather-app-mu-ten-48.vercel.app/)
- Backend API: [https://weatherapp-w2nz.onrender.com/](https://weatherapp-w2nz.onrender.com/)

---

## Features

### Weather Search

- Search by city, town, region, country, or postal code
- Select the correct location from search results
- Use the browser's current location
- Choose a date range from one to five days
- Choose Celsius or Fahrenheit

### Weather Information

- Current temperature
- Feels-like temperature
- Weather condition
- Humidity
- Wind speed
- Precipitation
- Daily minimum and maximum temperature
- Precipitation probability
- Sunrise and sunset
- Weather icons

### Air Quality and Travel Support

- U.S. Air Quality Index
- AQI category
- PM2.5
- PM10
- UV index
- Weather-based travel recommendations
- Google Maps link for the selected location

### Saved Weather Records

- Save a weather search to MongoDB
- View all saved records
- View a single record
- Update a saved record
- Delete a saved record
- Export records as JSON
- Export records as CSV

### Other Features

- Responsive design for desktop, tablet, and mobile
- Input validation
- Clear error messages
- Graceful handling when an external API is unavailable
- Swagger API documentation
- Automated backend tests

---

## Technology Stack

### Frontend

- React
- Vite
- React Router
- Axios
- JavaScript
- CSS
- CSS Grid
- Flexbox

### Backend

- Python
- FastAPI
- Pydantic
- PyMongo Async
- HTTPX
- Uvicorn

### Database

- MongoDB Atlas

### External Services

- Open-Meteo Geocoding API
- Open-Meteo Forecast API
- Open-Meteo Air Quality API
- Google Maps URL integration

### Deployment

- Vercel for the frontend
- Render for the backend
- MongoDB Atlas for database storage

---

## How the Application Works

```text
User
  |
  v
React Frontend
  |
  | Axios requests
  v
FastAPI Backend
  |
  |---- Open-Meteo Geocoding API
  |---- Open-Meteo Forecast API
  |---- Open-Meteo Air Quality API
  |
  v
MongoDB Atlas
```

### Weather Search Flow

1. The user enters a location or selects the current-location option.
2. The React frontend sends the request to FastAPI.
3. FastAPI validates the request.
4. The backend searches for matching locations using Open-Meteo.
5. The user selects the correct location.
6. FastAPI retrieves weather and air-quality data.
7. The frontend displays current conditions, forecast cards, air quality, and travel recommendations.

### Save Record Flow

1. The user searches for weather information.
2. The user selects **Save Weather Search**.
3. React sends the location, date range, and temperature unit to FastAPI.
4. FastAPI validates the request.
5. Fresh weather information is retrieved.
6. The result is stored in MongoDB Atlas.
7. The saved record appears on the Saved Records page.

### Update Record Flow

1. The user opens a saved record.
2. The user changes the location, date range, or temperature unit.
3. React sends a PATCH request to FastAPI.
4. FastAPI validates the new values.
5. Fresh weather information is retrieved.
6. MongoDB is updated with the latest result.

---

## Project Structure

```text
WeatherApp/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── locations.py
│   │   │   ├── weather.py
│   │   │   └── weather_records.py
│   │   ├── services/
│   │   │   ├── air_quality_service.py
│   │   │   ├── location_service.py
│   │   │   ├── weather_service.py
│   │   │   └── weather_record_service.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── Scripts/
│   │   └── check_mongodb.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   ├── vercel.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns basic API information |
| GET | `/api/health` | Checks API and MongoDB health |

### Location and Weather

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/locations/search` | Searches for matching locations |
| GET | `/api/weather` | Retrieves current weather and forecast |
| GET | `/api/air-quality` | Retrieves current air-quality information |

### Weather Records

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/weather-records` | Creates a weather record |
| GET | `/api/weather-records` | Returns all saved records |
| GET | `/api/weather-records/{record_id}` | Returns one saved record |
| PATCH | `/api/weather-records/{record_id}` | Updates a saved record |
| DELETE | `/api/weather-records/{record_id}` | Deletes a saved record |

### Export

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/weather-records/export/json` | Downloads saved records as JSON |
| GET | `/api/weather-records/export/csv` | Downloads saved records as CSV |

Swagger documentation is available locally at:

```text
http://127.0.0.1:8000/docs
```

---

## Validation Rules

The backend uses Pydantic to validate incoming requests.

The main validation rules are:

- Location must contain at least two characters
- Either a location or a complete latitude and longitude pair must be provided
- Latitude must be between `-90` and `90`
- Longitude must be between `-180` and `180`
- Start date cannot be in the past
- End date cannot be earlier than the start date
- Date range cannot exceed five days
- Temperature unit must be Celsius or Fahrenheit
- Unexpected request fields are rejected

The backend uses the configured application timezone when validating dates.

---

## Local Setup

### Requirements

Install the following tools before running the project:

- Python 3.12 or later
- Node.js
- npm
- Git
- A MongoDB Atlas account

Clone the repository:

```bash
git clone https://github.com/rajaraman04/WeatherApp
cd WeatherApp
```

---

## Backend Setup

Open a terminal from the project root:

```bash
cd backend
```

### Create a virtual environment

#### Windows PowerShell

```powershell
py -m venv tech
.\tech\Scripts\Activate.ps1
```

#### macOS or Linux

```bash
python3 -m venv tech
source tech/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create the environment file

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

#### macOS or Linux

```bash
cp .env.example .env
```

Update `backend/.env` with your MongoDB Atlas connection string.

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/?retryWrites=true&w=majority&appName=WeatherApp
MONGODB_DATABASE=WeatherApp
MONGODB_COLLECTION=Weather_records

GEOCODING_API_URL=https://geocoding-api.open-meteo.com/v1/search
FORECAST_API_URL=https://api.open-meteo.com/v1/forecast
AIR_QUALITY_API_URL=https://air-quality-api.open-meteo.com/v1/air-quality

EXTERNAL_API_TIMEOUT_SECONDS=10
APP_TIMEZONE=America/New_York

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173
```

Do not commit the real `.env` file.

### Start the backend

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## MongoDB Connection Check

The project includes a small script for checking the MongoDB connection.

From the `backend` folder, run:

```bash
python Scripts/check_mongodb.py
```

The script reads the MongoDB connection string from `backend/.env`.

It should only display whether the connection succeeded or failed. It should not print the complete MongoDB URI.

---

## Frontend Setup

Open another terminal from the project root:

```bash
cd frontend
```

### Install dependencies

```bash
npm install
```

### Create the frontend environment file

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

#### macOS or Linux

```bash
cp .env.example .env
```

Add the local backend URL:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Start the frontend

```bash
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

## Production Build

Create a production build:

```bash
cd frontend
npm run build
```

Test the production build locally:

```bash
npm run preview
```

Vite preview normally runs at:

```text
http://localhost:4173
```

The FastAPI CORS configuration must allow port `4173` for preview requests.

---

## Testing

### Backend Tests

From the `backend` folder:

```bash
pytest -v
```

The test suite covers areas such as:

- Root endpoint
- Health endpoint
- Request validation
- Location validation
- Coordinate validation
- Date-range validation
- Weather data parsing
- Air-quality response parsing
- AQI category calculation
- CRUD behavior
- Export behavior

### Frontend Validation

From the `frontend` folder:

```bash
npm run lint
npm run build
```

Both commands should complete without errors before deployment or submission.

---

## Application Pages

### Dashboard

The Dashboard allows users to:

- Search for a location
- Use their current location
- Choose a date range
- Select Celsius or Fahrenheit
- View current conditions
- View air quality
- View travel recommendations
- Open the location in Google Maps
- Save the weather search
- View the daily forecast

### Saved Records

The Saved Records page allows users to:

- View stored weather records
- Update a record
- Delete a record
- Export records as JSON
- Export records as CSV

### About

The About page contains information about:

- WeatherWise
- The developer
- The technology stack
- Product Manager Accelerator

### Not Found

The Not Found page handles unknown frontend routes.

---

## Air-Quality Integration

WeatherWise uses the Open-Meteo Air Quality API.

The dashboard displays:

- U.S. Air Quality Index
- AQI category
- PM2.5
- PM10
- UV index

Air-quality data is provided by Open-Meteo and CAMS ENSEMBLE.

Air quality is treated as an additional feature. If the air-quality request fails, the main weather and forecast sections continue to work.

---

## Travel Recommendations

WeatherWise creates simple travel recommendations using:

- Rain probability
- Maximum temperature
- Air Quality Index
- UV index

Recommendations may include:

- Carrying an umbrella when rain is likely
- Carrying water during hot conditions
- Using sunscreen when the UV index is high
- Limiting long outdoor activities when air quality is poor

These recommendations are general planning suggestions. They are not medical advice or emergency alerts.

---

## Google Maps Integration

The selected location can be opened in Google Maps using its latitude and longitude.

This feature uses a Google Maps URL and does not require a separate Google Maps API key.

---

## Responsive Design

WeatherWise supports desktop, tablet, and mobile screens.

The layout uses:

- CSS Grid
- Flexbox
- Flexible container widths
- Responsive cards
- Tablet and mobile media queries
- Stacked forms and buttons on small screens

---

## Error Handling

The application handles common errors such as:

- Invalid location input
- No matching location results
- Past dates
- Date ranges longer than five days
- Invalid latitude or longitude
- Browser location permission denied
- Browser location unavailable
- External API timeout
- MongoDB connection failure
- Air-quality service failure
- Backend connection failure

Clear messages are shown to help the user understand what went wrong.

---

## Data Export

Saved MongoDB records can be exported in two formats.

### JSON Export

```text
GET /api/weather-records/export/json
```

The JSON file contains the complete stored weather records.

### CSV Export

```text
GET /api/weather-records/export/csv
```

The CSV file can be opened using spreadsheet applications such as Microsoft Excel or Google Sheets.

---


## Deployment

### Frontend Deployment

The React frontend is deployed on Vercel.

The following environment variable is configured in Vercel:

```env
VITE_API_BASE_URL=https://weatherapp-w2nz.onrender.com/
```

Vercel uses the following frontend settings:

```text
Root Directory: frontend
Framework: Vite
Build Command: npm run build
Output Directory: dist
```

The `frontend/vercel.json` file redirects React Router paths to `index.html`.

### Backend Deployment

The FastAPI backend is deployed on Render.

Render uses:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /api/health
```

Backend environment variables are configured directly in Render.

The production Vercel URL must be included in the backend `CORS_ORIGINS` variable.

### Database Deployment

MongoDB Atlas stores saved weather records.

Render's outbound IP ranges must be added to the MongoDB Atlas Network Access list so the deployed backend can connect to the database.

---

## Environment Variables

### Backend

| Variable | Purpose |
|---|---|
| `MONGODB_URI` | MongoDB Atlas connection string |
| `MONGODB_DATABASE` | MongoDB database name |
| `MONGODB_COLLECTION` | MongoDB collection name |
| `GEOCODING_API_URL` | Open-Meteo geocoding endpoint |
| `FORECAST_API_URL` | Open-Meteo forecast endpoint |
| `AIR_QUALITY_API_URL` | Open-Meteo air-quality endpoint |
| `EXTERNAL_API_TIMEOUT_SECONDS` | External API timeout |
| `APP_TIMEZONE` | Timezone used for date validation |
| `CORS_ORIGINS` | Frontend origins allowed to access FastAPI |

### Frontend

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the FastAPI backend |

---

## Known Limitations

- Historical weather for past dates is not supported
- Forecast date ranges are limited to five days
- Air-quality information may occasionally be unavailable
- Browser geolocation requires user permission
- Browser geolocation requires HTTPS in production
- Travel recommendations are general suggestions
- The free Render backend may take time to restart after inactivity
- The application does not currently support user accounts

---

## Future Improvements

Possible future improvements include:

- User authentication
- Favorite locations
- Hourly forecasts
- Historical weather
- Weather alerts
- Interactive maps
- More export formats
- Saved-record pagination
- Dark mode
- Improved accessibility
- Personalized travel recommendations

---

## Developer

**Rajaraman Rajagopalan**

M.S. in Computer Science  
Binghamton University

---

## Product Manager Accelerator

Product Manager Accelerator supports product-management professionals at different stages of their careers.

The organization provides learning and career-development support through areas such as:

- Product-management training
- Career preparation
- Mock interviews
- Leadership development
- AI product-management programs

This project was created as part of the Product Manager Accelerator technical assessment.

---

