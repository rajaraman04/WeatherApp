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