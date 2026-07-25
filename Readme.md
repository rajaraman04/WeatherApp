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