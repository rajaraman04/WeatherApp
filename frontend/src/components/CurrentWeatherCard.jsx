import {getTemperatureSymbol,getWeatherIcon,getWindUnitLabel,} from "../utils/weather.js";

function displayValue(value, suffix = "") {
  if (value === null || value === undefined) {
    return "Not available";
  }
  return `${value}${suffix}`;
}

function CurrentWeatherCard({location,weatherData,}) {
  const currentWeather =weatherData.current_weather;
  if (!currentWeather) {
    return (
      <article className="content-card">
        <p className="eyebrow">Current conditions</p>
        <h2>Current weather is unavailable</h2>
      </article>
    );
  }

  const temperatureSymbol = getTemperatureSymbol(weatherData.temperature_unit,);

  const locationLabel = [location.name,location.state,location.country,].filter(Boolean).join(", ");

  return (
    <article className="content-card current-weather-card">
      <p className="eyebrow">Current conditions</p>
      <div className="current-weather__header">
        <div>
          <h2>{locationLabel}</h2>
          <p className="muted-text">
            {currentWeather.condition}
          </p>
          {location.isCurrentLocation && (
            <p className="current-location-label">
                Detected using browser location
            </p>
            )}
        </div>

        <span className="current-weather__icon" aria-hidden="true">
          {getWeatherIcon(
            currentWeather.weather_code,
          )}
        </span>
      </div>

      <div className="current-weather__temperature">
        {currentWeather.temperature}
        {temperatureSymbol}
      </div>

      <div className="weather-metrics">
        <div className="weather-metric">
          <span>Feels like</span>
          <strong>
            {displayValue(currentWeather.feels_like,temperatureSymbol,)}
          </strong>
        </div>

        <div className="weather-metric">
          <span>Humidity</span>
          <strong>
            {displayValue(currentWeather.humidity,"%",)}
          </strong>
        </div>

        <div className="weather-metric">
          <span>Wind</span>
          <strong>
            {displayValue(currentWeather.wind_speed,` ${getWindUnitLabel(weatherData.wind_speed_unit,)}`,)}
          </strong>
        </div>

        <div className="weather-metric">
          <span>Precipitation</span>
          <strong>
            {displayValue(currentWeather.precipitation,` ${weatherData.precipitation_unit}`,)}
          </strong>
        </div>
      </div>
    </article>
  );
}
export default CurrentWeatherCard;