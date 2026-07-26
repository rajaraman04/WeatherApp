import { useState } from "react";

import ForecastSection from "../components/ForecastSection.jsx";
import CurrentWeatherCard from "../components/CurrentWeatherCard.jsx";
import LocationResults from "../components/LocationResults.jsx";
import LocationSearchForm from "../components/LocationSearchForm.jsx";
import SaveWeatherPanel from "../components/SaveWeatherPanel.jsx";
import TravelExtras from "../components/TravelExtras.jsx";
import {createWeatherRecord, getAirQuality,getWeather,searchLocations,} from "../services/api.js";
import { getApiErrorMessage } from "../utils/apiError.js";
import { getCurrentCoordinates } from "../utils/geolocation.js";

function Dashboard() {
  const [locationResults, setLocationResults] =useState([]);
  const [searchCriteria, setSearchCriteria] =useState(null);
  const [selectedLocation, setSelectedLocation] =useState(null);
  const [weatherData, setWeatherData] =useState(null);
  const [isSearching, setIsSearching] =useState(false);
  const [isLoadingWeather, setIsLoadingWeather] =useState(false);
  const [isLocating, setIsLocating] =useState(false);
  const [errorMessage, setErrorMessage] =useState("");
  const [isSaving, setIsSaving] =useState(false);
  const [savedRecordId, setSavedRecordId] =useState(null);
  const [saveMessage, setSaveMessage] =useState("");
  const [airQuality, setAirQuality] =useState(null);  
  function resetSaveState() {
  setIsSaving(false);
  setSavedRecordId(null);
  setSaveMessage("");
}

  async function handleLocationSearch(criteria) {
    setIsSearching(true);
    setErrorMessage("");
    setLocationResults([]);
    setSelectedLocation(null);
    setWeatherData(null);
    resetSaveState();
    setAirQuality(null);
    try {
      const results = await searchLocations(criteria.location,);
      setSearchCriteria(criteria);
      setLocationResults(results);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error),);
    } finally {
      setIsSearching(false);
    }
  }

  async function handleLocationSelection(location) {
    if (!searchCriteria) {
      return;
    }
    setIsLoadingWeather(true);
    setErrorMessage("");
    setAirQuality(null);
    resetSaveState();
    try {
      const weatherRequest = getWeather({latitude: location.latitude,longitude: location.longitude,startDate: searchCriteria.startDate,endDate: searchCriteria.endDate,temperatureUnit:searchCriteria.temperatureUnit,});
      const airQualityRequest = getAirQuality({latitude: location.latitude,longitude: location.longitude,}).catch(() => null);
      const [weatherResult,airQualityResult,] = await Promise.all([weatherRequest,airQualityRequest,]);
      setSelectedLocation(location);
      setWeatherData(weatherResult);
      setAirQuality(airQualityResult);
      setLocationResults([]);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error),);
    } finally {
      setIsLoadingWeather(false);
    }
  }

async function handleCurrentLocation(criteria) {
  setIsLocating(true);
  setErrorMessage("");
  setLocationResults([]);
  setSelectedLocation(null);
  setWeatherData(null);
  resetSaveState();
  setAirQuality(null);
  try {
    const coordinates = await getCurrentCoordinates();
    const weatherRequest = getWeather({latitude: coordinates.latitude,longitude: coordinates.longitude,startDate: criteria.startDate,endDate: criteria.endDate,temperatureUnit:criteria.temperatureUnit,});
    const airQualityRequest = getAirQuality({latitude: coordinates.latitude,longitude: coordinates.longitude,}).catch(() => null);

    const [weatherResult,airQualityResult,]=await Promise.all([weatherRequest,airQualityRequest,]);
    setSearchCriteria({location: null,...criteria,});
    setSelectedLocation({name: "Current location",state: null,country: null,postal_code: null,latitude: coordinates.latitude,longitude: coordinates.longitude,accuracy: coordinates.accuracy,isCurrentLocation: true,});

    setWeatherData(weatherResult);
    setAirQuality(airQualityResult)
  } catch (error) {
    if (error.name === "BrowserGeolocationError") {
      setErrorMessage(error.message);
    } else {
      setErrorMessage(getApiErrorMessage(error),);
    }
  } finally {
    setIsLocating(false);
  }
}

function buildWeatherRecordRequest() {
  if (!searchCriteria ||!selectedLocation ||!weatherData) {
    return null;
  }

  const requestData = {start_date: searchCriteria.startDate,end_date: searchCriteria.endDate,temperature_unit:searchCriteria.temperatureUnit,};

  if (selectedLocation.isCurrentLocation) {
    return {...requestData,latitude: selectedLocation.latitude,longitude: selectedLocation.longitude,};
  }

  return {...requestData,location: searchCriteria.location,};
}

async function handleSaveWeather() {
  const requestData =buildWeatherRecordRequest();
  if (!requestData) {
    setSaveMessage("Search for weather before saving a record.",);
    return;
  }

  setIsSaving(true);
  setSaveMessage("");

  try {
    const savedRecord =await createWeatherRecord(requestData);
    setSavedRecordId(savedRecord.id);

    setSaveMessage("Weather search saved successfully.",);
  } catch (error) {
    setSavedRecordId(null);
    setSaveMessage(getApiErrorMessage(error),);
  } finally {
    setIsSaving(false);
  }
}

  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">
            Real-time Weather Planning App
          </p>

          <h1>
            Plan confidently with weather that matters.
          </h1>

          <p className="hero__description">
            Search any location in the globe, review current conditions, and compare a five-day forecast before making travel plans.
          </p>
        </div>

        <div
          className="hero__summary" aria-label="Project capabilities">
          <div>
            <strong>5-day</strong>
            <span>forecast</span>
          </div>

          <div>
            <strong>Live</strong>
            <span>weather data</span>
          </div>

          <div>
            <strong>CRUD</strong>
            <span>saved records</span>
          </div>
        </div>
      </section>

    <LocationSearchForm isLocating={isLocating} isSearching={isSearching} onSearch={handleLocationSearch} onUseCurrentLocation={handleCurrentLocation}/>
      {errorMessage && ( <div className="error-alert" role="alert">
          {errorMessage}
        </div>
      )}

      <LocationResults isLoadingWeather={isLoadingWeather}  locations={locationResults} onSelect={handleLocationSelection}/>

      {weatherData && selectedLocation ? (
        <section className="weather-overview-grid" aria-label="Weather overview">
          <CurrentWeatherCard location={selectedLocation} weatherData={weatherData}/>
          <TravelExtras airQuality={airQuality} location={selectedLocation} weatherData={weatherData}/>
          <SaveWeatherPanel isSaving={isSaving} onSave={handleSaveWeather} savedRecordId={savedRecordId} saveMessage={saveMessage}/>
        </section>
      ) : (
        <section className="weather-overview-grid">
          <article className="content-card current-weather-card">
            <p className="eyebrow">Current conditions</p>
            <h2>No weather selected</h2>
            <p className="muted-text">
              Search for a location to view temperature,humidity, wind speed, precipitation, and current conditions.
            </p>
            <div className="weather-placeholder">
              <span aria-hidden="true">☁</span>
              <strong>--°</strong>
            </div>
          </article>
        </section>
      )}
      <ForecastSection weatherData={weatherData} />
    </>
  );
}
export default Dashboard;