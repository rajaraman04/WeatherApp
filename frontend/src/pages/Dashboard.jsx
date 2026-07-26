import { useState } from "react";

import CurrentWeatherCard from "../components/CurrentWeatherCard.jsx";
import LocationResults from "../components/LocationResults.jsx";
import LocationSearchForm from "../components/LocationSearchForm.jsx";
import {getWeather,searchLocations,} from "../services/api.js";
import { getApiErrorMessage } from "../utils/apiError.js";

const forecastPlaceholders = ["Day 1","Day 2","Day 3","Day 4","Day 5",];

function Dashboard() {
  const [locationResults, setLocationResults] =useState([]);
  const [searchCriteria, setSearchCriteria] =useState(null);
  const [selectedLocation, setSelectedLocation] =useState(null);
  const [weatherData, setWeatherData] =useState(null);
  const [isSearching, setIsSearching] =useState(false);
  const [isLoadingWeather, setIsLoadingWeather] =useState(false);
  const [errorMessage, setErrorMessage] =useState("");
  async function handleLocationSearch(criteria) {
    setIsSearching(true);
    setErrorMessage("");
    setLocationResults([]);
    setSelectedLocation(null);
    setWeatherData(null);
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
    try {
      const result = await getWeather({latitude: location.latitude,longitude: location.longitude,startDate: searchCriteria.startDate,endDate: searchCriteria.endDate,temperatureUnit:searchCriteria.temperatureUnit,});
      setSelectedLocation(location);
      setWeatherData(result);
      setLocationResults([]);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error),);
    } finally {
      setIsLoadingWeather(false);
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

      <LocationSearchForm isSearching={isSearching} onSearch={handleLocationSearch}/>

      {errorMessage && ( <div className="error-alert" role="alert">
          {errorMessage}
        </div>
      )}

      <LocationResults isLoadingWeather={isLoadingWeather}  locations={locationResults} onSelect={handleLocationSelection}/>

      <section className="dashboard-grid">
        {weatherData && selectedLocation ? (
          <CurrentWeatherCard location={selectedLocation} weatherData={weatherData}/>) : (
          <article className="content-card current-weather-card">
            <p className="eyebrow">
              Current conditions
            </p>

            <h2>No weather selected</h2>

            <p className="muted-text">
              Search for a location to view temperature, humidity, wind speed, precipitation, and current conditions.
            </p>

            <div className="weather-placeholder">
              <span aria-hidden="true">☁</span>
              <strong>--°</strong>
            </div>
          </article>
        )}

        <article className="content-card">
          <p className="eyebrow">Travel guidance</p>
          <h2>Smart travel insights</h2>

          <p className="muted-text">
            Weather-based recommendations for rain, UV exposure, air quality, wind, heat, and cold will appear here.
          </p>

          <ul className="insight-list">
            <li>Umbrella recommendation</li>
            <li>Clothing guidance</li>
            <li>Outdoor-activity suitability</li>
          </ul>
        </article>
      </section>

      <section className="content-card forecast-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">
              Upcoming conditions
            </p>

            <h2>Five-day forecast</h2>
          </div>

          <p className="section-heading__description">
            The forecast response is now available in React state. Its complete display will be implemented soon.
          </p>
        </div>

        <div className="forecast-grid">
          {forecastPlaceholders.map((day) => (
            <article className="forecast-card" key={day}>
              <strong>{day}</strong>
              <span className="forecast-card__icon" aria-hidden="true">
                ◌
              </span>
              <span>High: --°</span>
              <span>Low: --°</span>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
export default Dashboard;