import {formatForecastDate,formatWeatherTime,} from "../utils/date.js";

import {formatWeatherNumber,getPrecipitationUnitLabel,getTemperatureSymbol,getWeatherIcon,getWindUnitLabel,} from "../utils/weather.js";

function displayPrecipitationProbability(value) {
  if (value === null || value === undefined) {
    return "Not available";
  }
  return `${formatWeatherNumber(value, 0)}%`;
}

function ForecastCard({forecastDay,precipitationUnit,temperatureUnit,windSpeedUnit,}) {
  const { weekday, dateLabel } =formatForecastDate(forecastDay.forecast_date,);

  const temperatureSymbol =getTemperatureSymbol(temperatureUnit);

  const precipitationUnitLabel =getPrecipitationUnitLabel(precipitationUnit,);

  const windUnitLabel =getWindUnitLabel(windSpeedUnit);

  return (
    <article className="forecast-card forecast-card--real">
      <div className="forecast-card__header">
        <div>
          <h3>{weekday}</h3>
          <p>{dateLabel}</p>
        </div>

        <span className="forecast-card__weather-icon" aria-hidden="true">
          {getWeatherIcon(forecastDay.weather_code,)}
        </span>
      </div>

      <p className="forecast-card__condition">
        {forecastDay.condition ?? "Condition unavailable"}
      </p>

      <div className="forecast-card__temperatures">
        <div>
          <span>High</span>

          <strong>
            {formatWeatherNumber( forecastDay.maximum_temperature,)}
            {temperatureSymbol}
          </strong>
        </div>

        <div>
          <span>Low</span>

          <strong>
            {formatWeatherNumber(forecastDay.minimum_temperature,)}
            {temperatureSymbol}
          </strong>
        </div>
      </div>

      <dl className="forecast-details">
        <div>
          <dt>Rain chance</dt>

          <dd>
            {displayPrecipitationProbability(forecastDay.precipitation_probability,)}
          </dd>
        </div>

        <div>
          <dt>Precipitation</dt>
          <dd>
            {formatWeatherNumber(forecastDay.precipitation_sum,2,)}{" "}
            {precipitationUnitLabel}
          </dd>
        </div>

        <div>
          <dt>Max wind</dt>
          <dd>
            {formatWeatherNumber(forecastDay.maximum_wind_speed,)}{" "}
            {windUnitLabel}
          </dd>
        </div>

        <div>
          <dt>Sunrise</dt>
          <dd>
            {formatWeatherTime(forecastDay.sunrise,)}
          </dd>
        </div>

        <div>
          <dt>Sunset</dt>
          <dd>
            {formatWeatherTime(forecastDay.sunset,)}
          </dd>
        </div>
      </dl>
    </article>
  );
}
export default ForecastCard;